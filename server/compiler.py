import os
import subprocess
import requests
import shutil

def download_files_from_github(repo_url, file_list, download_dir="."):
    downloaded = []
    for file in file_list:
        url = f"{repo_url}/{file}"
        local_path = os.path.join(download_dir, file)

        # Ensure subdirectories exist (e.g., headers/)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                downloaded.append(local_path)
                print(f"[+] Downloaded {file}")
            else:
                print(f"[-] Failed to download {file}: {response.status_code}")
                return None
        except Exception as e:
            print(f"[-] Error downloading {file}: {e}")
            return None
    return downloaded

def compile_agent(ip, port, enable_all=False, enable_save_file=False, enable_daemon_file=False):
    base_url = "https://raw.githubusercontent.com/Matthew-a-smith/Agent/main"
    c_files = ["main.c", "utils.c", "track.c", "finder.c", "process.c", "decompile.c", "proxy.c"]
    header_files = [
        "headers/binarys.h", "headers/finder.h", "headers/track.h", 
        "headers/process_info.h", "headers/decompile.h", "headers/utils.h", "headers/proxy.h",
        "headers/process_final_tracker.h", "headers/suspicious.h",
    ]
    external_files = ["externals/uthash.h"]

    all_files = c_files + header_files + external_files

    # Download all source files
    downloaded = download_files_from_github(base_url, all_files)
    if not downloaded:
        print("[-] File download failed.")
        return

    # Compile with include paths for headers and externals
    compile_cmd = [
        "gcc", *c_files,
        "-Iheaders", "-Iexternals",
        f'-DPROXY_IP="{ip}"',
        f'-DPROXY_PORT={port}',
        "-o", "agent_p", "-lssl", "-lcrypto"
    ]

    if enable_all:
        compile_cmd.append("-DLOG_ENABLED")
    if enable_save_file:
        compile_cmd.append("-DSAVE_ENABLED")
    if enable_daemon_file:
        compile_cmd.append("-DDAEMON_ENABLED")

    result = subprocess.run(compile_cmd, capture_output=True, text=True)

    # Cleanup source and header files
    for f in c_files:
        os.remove(f)
    if os.path.exists("headers"):
        shutil.rmtree("headers")
    if os.path.exists("externals"):
        shutil.rmtree("externals")

    # Output result
    if result.returncode == 0:
        print("[+] Compilation successful.")
    else:
        print("[-] Compilation failed:")
        print(result.stderr)
