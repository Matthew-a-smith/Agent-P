from .constants import *
from globals import seen_bash_patterns
from .file_utils import save_filename_to_bash, save_file_to_bash

# Colorization function
def colorize_value(value, field_type):
    if field_type == "pid":
        return f"{CYAN}{value}{RESET}"
    elif field_type == "state":
        return f"{GREEN if value == 'ESTABLISHED' else RED}{value}{RESET}"
    elif field_type == "memory":
        try:
            mem_kb = int(value.split()[0])
            return f"{RED if mem_kb > 10000 else CYAN}{value}{RESET}"
        except:
            return value
    elif field_type == "protocol":
        return f"{YELLOW}{value}{RESET}"
    elif field_type == "address":
        return f"{BLUE}{value}{RESET}"
    elif field_type == "checksum":
        return f"{MAGENTA}{value}{RESET}"
    else:
        return value
    
def print_connection_info(conn):
    print(f"{BOLD}{MAGENTA}--- Suspicious Connection ---{RESET}")
    print(f"{BOLD}PID:{RESET} {colorize_value(conn['PID'], 'pid')}")
    print(f"{BOLD}Protocol:{RESET} {colorize_value(conn['Protocol'], 'protocol')}")
    print(f"{BOLD}Local Address:{RESET} {colorize_value(conn['Local Address'], 'address')}")
    print(f"{BOLD}Remote Address:{RESET} {colorize_value(conn['Remote Address'], 'address')}")
    print(f"{BOLD}State:{RESET} {colorize_value(conn['State'], 'state')}")
    print(f"{BOLD}Start Time:{RESET} {conn['Start Time']}")


def print_decompile_info(info):
    print(f"{BOLD}{MAGENTA}--- Decompilation Info ---{RESET}")
    for key, val in info.items():
        print(f"{BOLD}{key}:{RESET} {val}")

seen_bash_patterns = set()

def print_bash_info(info):
    pattern = info['Pattern']
    if pattern in seen_bash_patterns:
        return
    seen_bash_patterns.add(pattern)
    print(f"{BOLD}Detected:{RESET} {pattern}")

# Print formatted process processes
def print_process_processes(processes, addr):
    print(f"{BOLD}{RED}<--- Processes info --->{RESET} {BOLD}{LIGHT_BLUE}{addr[0]}{RESET}")
    print(f"{BOLD}Start Time:{RESET} {processes['Start Time']}  "
          f"{BOLD}PID:{RESET} {colorize_value(processes['PID'], 'pid')}  "
          f"{BOLD}Process Name:{RESET} {colorize_value(processes['Process Name'], 'protocol')}  "
          f"{BOLD}Parent PID:{RESET} {colorize_value(processes['Parent PID'], 'pid')}  "
          f"{BOLD}Memory:{RESET} {colorize_value(processes['Memory'], 'memory')}  "
          f"{BOLD}CMD:{RESET} {colorize_value(processes['CMD'], 'address')}")
    print(f"{BOLD}User:{RESET} {processes['User']}")
    print(f"{BOLD}Executable Path:{RESET} {processes['Executable Path']}")
    print(f"{BOLD}Checksum:{RESET} {colorize_value(processes['Checksum'], 'checksum')}")
    print(f"{BOLD}Source Path:{RESET} {processes['Source Path']}")
    print(f"{BOLD}Source Checksum:{RESET} {colorize_value(processes['Source Checksum'], 'checksum')}")
    print(f"{BOLD}Saved File:{RESET} {processes['Saved File']}")
    print(f"{BOLD}Command to execute:{RESET} {processes['CMD']}")
    save_filename_to_bash(processes['Source Path'])
    save_file_to_bash(processes['Process Name'], processes['User'])
