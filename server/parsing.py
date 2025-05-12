import re

# Parse block of process info
def parse_process_block(lines):
    processes = {
        "Start Time": "", "PID": "", "Process Name": "", "Parent PID": "",
        "Memory": "", "CMD": "", "Executable Path": "", "Checksum": "",
        "Source Path": "", "Source Checksum": "", "Saved File": "",
        "User": "",
    }
    for line in lines:
        match = re.match(r"(\w[\w\s]+):\s+(.*)", line)
        if match:
            key, value = match.groups()
            if key in processes:
                processes[key] = value
    return processes

def parse_decompile_block(lines):
    decompile_info = {
        "FilePath": "",
        "Entry Point": "",
        "Program Header Offset": "",
        "Section Header Offset": "",
    }
    for line in lines:
        match = re.match(r"(\w[\w\s]+):\s+(.*)", line)
        if match:
            key, value = match.groups()
            if key in decompile_info:
                decompile_info[key] = value
    return decompile_info

def parse_bash_block(lines):
    bash_info = {
        "Pattern": ""
    }
    for line in lines:
        match = re.match(r"Pattern:\s+\((.*?)\)\s+→\s+(.*)", line)
        if match:
            pattern, command = match.groups()
            bash_info["Pattern"] = f"({pattern}) → {command}"
    return bash_info

def parse_connection_block(lines):
    conn_info = {
        "PID": "",
        "Protocol": "",
        "Local Address": "",
        "Remote Address": "",
        "State": "",
        "Start Time": ""
    }
    for line in lines:
        match = re.match(r"(\w[\w\s]+):\s+(.*)", line)
        if match:
            key, value = match.groups()
            if key in conn_info:
                conn_info[key] = value
    return conn_info
enable_logs = False
