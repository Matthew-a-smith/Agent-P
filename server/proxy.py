# proxy.py
import socket
import errno
import globals 
from .parsing import *
from .printer import *

# === Proxy Handler ===
def handle_client(client_socket, client_address):
    # Check if the connection is already in the set
    if client_address[0] not in globals.open_connections:
        globals.open_connections.add(client_address[0])
        print(f"[+] New connection from {client_address[0]}")

    try:
        while True:
            # === If there is a pending file, send it ===
            if globals.pending_files:
                source_path, dest_path = globals.pending_files.pop(0)
                print(f"[+] Sending file {source_path} to {dest_path}")

                with open(source_path, "rb") as f:
                    file_data = f.read()

                dest_path_bytes = dest_path.encode()
                client_socket.sendall(b'\x02')  # 0x01 indicates command mode
                client_socket.sendall(len(dest_path_bytes).to_bytes(4, 'big'))
                client_socket.sendall(dest_path_bytes)
                client_socket.sendall(len(file_data).to_bytes(8, 'big'))
                client_socket.sendall(file_data)

                print(f"[+] File {source_path} sent to {dest_path}")

            if globals.pending_cmd:
                source_cmd, dest_path = globals.Spending_cmd.pop(0)
                print(f"[+] Sending cmd {source_cmd} to {dest_path}")

                dest_path_bytes = dest_path.encode()
                dest_cmd_bytes = source_cmd.encode()

                client_socket.sendall(b'\x01')  # 0x01 indicates command mode
                client_socket.sendall(len(dest_path_bytes).to_bytes(4, 'big'))
                client_socket.sendall(dest_path_bytes)
                client_socket.sendall(len(dest_cmd_bytes).to_bytes(8, 'big'))
                client_socket.sendall(dest_cmd_bytes)

                print(f"[+] Cmd {source_cmd} sent to {dest_path}")

            else:
                # No file to send — send 0
                client_socket.sendall((0).to_bytes(8, 'big'))

                # === Now wait for incoming data ===
                data = client_socket.recv(4096)
            if not data:
                pass
                break
            # Check if this is a file transfer header
            if b"[FILE_TRANSFER]" in data:
                try:
                    text_part = data.decode(errors="ignore")  # Only decode the header safely
                    lines = text_part.splitlines()

                    filename = None
                    file_size = None
                    header_length = 0

                    for i, line in enumerate(lines):
                        if line.startswith("FILENAME:"):
                            filename = line.split(":", 1)[1].strip()
                        elif line.startswith("SIZE:"):
                            file_size = int(line.split(":", 1)[1].strip())
                        if filename and file_size:
                            header_length = len("\n".join(lines[:i+1])) + 1  # +1 for final newline
                            break
                        
                    if not filename or not file_size:
                        print("[-] Malformed [FILE_TRANSFER] header")
                        continue
                    
                    # Calculate how many bytes remain (after header)
                    raw_data = data[header_length:]
                    while len(raw_data) < file_size:
                        raw_data += client_socket.recv(4096)

                    # Save the file
                    import os
                    os.makedirs("received_files", exist_ok=True)
                    save_path = os.path.join("received_files", filename)
                    with open(save_path, "wb") as f:
                        f.write(raw_data[:file_size])

                    print(f"[+] Received file saved to: {save_path}")

                    # If more data came after the file, continue processing it
                    remaining_data = raw_data[file_size:]
                    if remaining_data:
                        data = remaining_data
                    else:
                        continue  # Go back to top of recv loop
                    
                except Exception as e:
                    print(f"[-] Error receiving file: {e}")
                    continue
                

            lines = data.decode(errors="ignore").splitlines()
            block_type = None
            block_lines = []

            for line in lines:
                if "[Suspicious Process]" in line:
                    block_type = "suspicious"
                    block_lines = []
                elif "[Normal Process]" in line:
                    block_type = "normal"
                    block_lines = []
                elif "[Decompilation]" in line:
                    block_type = "decompile"
                    block_lines = []
                elif "[Suspicious Bash Pattern]" in line:
                    block_type = "bash"
                    block_lines = []
                elif "[Suspicious Connection]" in line:
                    block_type = "connection"
                    block_lines = []
                elif line.strip() == "":
                    if block_type and block_lines:
                        handle_block(block_type, block_lines, client_address)
                        block_type = None
                        block_lines = []
                else:
                    if block_type:
                        block_lines.append(line)

            if block_type and block_lines:
                handle_block(block_type, block_lines, client_address)

    except ConnectionResetError as e:
        if e.errno == errno.ECONNRESET:
            pass  # Or log less aggressively
        else:
            print(f"[-] Error handling client {client_address}: {e}")
    finally:
        client_socket.close()


def handle_block(block_type, block_lines, addr):
    if block_type == "suspicious" or block_type == "normal":
        parsed = parse_process_block(block_lines)
        print_process_processes(parsed, addr)
    elif block_type == "decompile":
        parsed = parse_decompile_block(block_lines)
        print_decompile_info(parsed)
    elif block_type == "bash":
        parsed = parse_bash_block(block_lines)
        print_bash_info(parsed)
    elif block_type == "connection":
        parsed = parse_connection_block(block_lines)
        print_connection_info(parsed)