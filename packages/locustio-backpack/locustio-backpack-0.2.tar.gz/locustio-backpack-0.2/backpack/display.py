


RED     = "\033[1;31m"  
BLUE    = "\033[1;34m"
CYAN    = "\033[1;36m"
GREEN   = "\033[0;32m"
YELLOW  = "\033[1;33m"
BLACK   = "\033[1;30m"
WHITE   = "\033[1;37m"
MAGENTA = "\033[1;35m"

RESET   = "\033[0;0m"
HRESET  = '\x1b[0m'
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

HGRN    = '\x1b[6;30;42m'
HBLU    = '\x1b[6;30;44m'
HBLACK  = '\x1b[6;30;40m'
HRED    = '\x1b[6;30;41m'
HYELLOW = '\x1b[6;30;43m'
HMAGENTA= '\x1b[6;30;45m'
HCYAN   = '\x1b[6;30;46m'
HWHITE  = '\x1b[6;30;47m'


def WARN(message):
    LBWA    = '[LOCUST BACKPACK WARNING]'
    MESG    = " " + message

    print(HYELLOW + LBWA + HRESET + RED + MESG + RESET)


def DEBUG(message):
    LBWA    = '[LOCUST BACKPACK DEBUG]'
    MESG    = " " + message

    print(HCYAN + LBWA + HRESET + YELLOW + MESG + RESET)

def SCALER(message):
    LBWA    = '[LOCUST BACKPACK AUTOSCALER]'
    MESG    = " " + message

    print(HGRN + LBWA + HRESET + BLUE + MESG + RESET)