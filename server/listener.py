# listener.py
import socket
import threading
import time
import globals
from .proxy import handle_client


# === Listener ===
def start_listener(host="127.0.0.1", port=4444):
    print(f"[+] Listening on {host}:{port}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    try:
        while globals.server_socket:
            try:
                client_sock, addr = server.accept()
                threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
                time.sleep(0.5)
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[*] Listener shutting down.")
    return server  # Return the server socket for later use