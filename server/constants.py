# constants.py
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
WHITE = "\x1b[37m"
ORANGE = "\x1b[38;5;214m"
BROWN = "\x1b[38;5;94m"
PINK = "\x1b[38;5;213m"
LIGHT_BLUE = "\x1b[38;5;153m"
LIGHT_GREEN = "\x1b[38;5;112m"
RESET = "\x1b[0m"
BOLD = "\x1b[1m"

def show_banner():
    print(
"\n"
f"{ORANGE} █████╗  ██████╗ ███████╗███╗   ██╗████████╗{RESET}{CYAN} ██████╗  {RESET}\n"
f"{ORANGE}██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝{RESET}{CYAN} ██╔══██╗ {RESET}\n"
f"{ORANGE}███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   {RESET}{CYAN} ██████╔╝ {RESET}\n"
f"{ORANGE}██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   {RESET}{CYAN} ██╔═══╝  {RESET}\n"
f"{ORANGE}██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   {RESET}{CYAN} ██║      {RESET}\n"
f"{ORANGE}╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   {RESET}{CYAN} ╚═╝      {RESET}\n"
    )