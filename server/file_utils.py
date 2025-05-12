# filename_saver.py
def save_filename_to_bash(file_path, bash_file_path="P4ck@p*nch.sh"):
    if "[NoneFound]" in file_path:
        return

    entry = f'    "{file_path}"'

    try:
        with open(bash_file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    new_lines = []
    inside_array = False
    already_present = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("file_paths=("):
            inside_array = True
            new_lines.append(line)
            continue

        if inside_array:
            if stripped == ")":
                if not already_present:
                    new_lines.append(entry + "\n")
                inside_array = False
            elif stripped == entry.strip():
                already_present = True
            new_lines.append(line)
        else:
            new_lines.append(line)

    # If file was empty or didn't contain the array, create it
    if not any("file_paths=(" in l for l in lines):
        new_lines = [
            "#!/bin/bash\n\n",
            "file_paths=(\n",
            f"{entry}\n",
            ")\n"
        ]

    with open(bash_file_path, "w") as f:
        f.writelines(new_lines)


def save_file_to_bash(file_name, file_owner, bash_file_path="P4ck@p*nch.sh"):
    if "[NoneFound]" in file_name:
        return  # Skip this file

    if "root" in file_owner:
        return  # Skip root-owned processes

    if "." in file_name:
        return  # Skip names that look like files (have extensions)

    entry = f'    "{file_name}"\n'

    try:
        with open(bash_file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return  # Do nothing if file doesn't exist

    new_lines = []
    inside_array = False
    already_present = False
    current_entries = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("file_names=("):
            inside_array = True
            new_lines.append(line)
            continue

        if inside_array:
            if stripped == ")":
                inside_array = False
                # Only add the entry if not already present and under 15 total
                if not already_present and len(current_entries) < 15:
                    current_entries.append(entry)
                new_lines.extend(current_entries)
                new_lines.append(line)
            elif stripped == entry.strip():
                already_present = True
                current_entries.append(line)
            elif stripped.startswith('"') and stripped.endswith('"'):
                current_entries.append(line)
        else:
            new_lines.append(line)

    with open(bash_file_path, "w") as f:
        f.writelines(new_lines)
