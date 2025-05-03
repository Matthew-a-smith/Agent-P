# file_utils.py
import os
import shutil
import globals
from server.constants import BOLD, RESET, GREEN, RED, YELLOW, CYAN


def save_file_to_address_directory(processes, addr):
    # Get the directory name from the Source Path or Saved File
    saved_file = processes.get("Saved File", "")

    # Create a directory named after the address (IP Address)
    directory_name = addr[0]  # addr[0] is the IP address
    directory_path = os.path.join(os.getcwd(), directory_name)
    os.makedirs(directory_path, exist_ok=True)

    # Now save the file into this directory
    destination_path = os.path.join(directory_path, os.path.basename(saved_file))

    try:
        if globals.enable_logs:
        # Copy the file to the new directory
            shutil.copy(saved_file, destination_path)
        return globals.enable_logs
    except Exception as e:
        print(f"Error while saving the file: {e}")