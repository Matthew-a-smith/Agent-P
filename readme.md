# Agent P
# Process Monitor

A lightweight Linux-based tool for monitoring processes, transferring files, and executing commands remotely. Built with C and Python, designed for red team and research use.

## Usage

## Set up the listener:
First, set the listener's IP and port using the --set lhost <ip> and --set lport <port> flags.
Then, start the listener using the --listener flag.

## Compile the agent:
Compile the agent using the --compile flag, including any additional compiler flags (--log, --save, --daemon) to adjust behavior.

## Send files or execute commands:
Use --send <local> <remote> to transfer files from your local system to the remote machine.
Use --run <cmd> <remote> to execute commands remotely.

## Listener behavior:
After sending files or commands, always ensure the listener is running to handle incoming requests. The listener will queue responses to send back once the request is received.

## Flags
 
| Flag                     | Purpose                                         |
|--------------------------|-------------------------------------------------|
| --set lhost <ip>         | Set the callback IP address                     |
| --set lport <port>       | Set the callback port                           |
| --show options           | Show current settings                           |
| --send <local> <remote>  | Send file from local path to remote address     |
| --run <cmd> <remote>     | Run commands on remote system                   |
| --compile                | Compile the agent with current settings         |
| --listener               | Start the listener server                       |
| exit                     | Exit the shell                                  |

| Compiler Flags | Description                                 |
|----------------|---------------------------------------------|
| --log          | Tracks all processes                        |
| --save         | Save source command if found to a file      |
| --daemon       | Run as a background process in memory       |

### Requirements
- Linux-based system
- GCC (for compilation)
- Root privileges (for full process/network access)
- Python for listener

Just set the listener address and compile with the flags you want. Depending on the compile-time flags, the listener behavior can change. Always set the listener after sending a command or file so it gets queued when a request is received to send back.




