from colorama import init, Fore, Style

init()  # initialize colorama


def ln(v: str):
    """
    Print a new message in prompt
    """
    print(v)


def err(v: str, e: Exception = None):
    """
    Print an error message
    """
    print(f"{Fore.RED}{v}: {e}{Style.RESET_ALL}")


def warn(v: str):
    """
    Print an warn message
    """
    print(f"{Fore.YELLOW}{v}{Style.RESET_ALL}")


def code(v: str):
    """
    Print an code formatted text
    """
    print(f"{Style.DIM}{v}{Style.RESET_ALL}")


def ask_yesno(self, question, default_yes=True):
    """ prompt the user for a yes/no question, when yes return true, false otherwise"""
    val = ln(f"{question} (y/n)? [{'y' if default_yes else 'n'}]")
    if val.strip().lower() in ['yes', 'y']:
        return True
    return False


def ask_int(self, question, min_val=0, max_val=None, def_val=None):
    """ prompt user for a int value, keep asking until a correct value is entered"""
    val = ""
    while True:
        try:
            val = input(question)
            # if there is a default value use it
            if not val and def_val is not None:
                val = def_val
                break
            # else check the boundaries
            if int(val) < min_val or (max_val is not None and int(val) > max_val):
                raise ValueError("")
            break
        except ValueError:
            if max_val is not None:
                print("sorry boss, choose something between %d and %d" %
                      (min_val, max_val))
            else:
                print("sorry boss, chose a number greater than %d" %
                      (min_val))
    return val


def ask_str(self, question, default_val=""):
    """ read a string from a command line, apply default_val if the input is empty"""
    val = input(question).strip()
    if not val:
        val = default_val
    return val
