import os
import sys
from colorama import Fore
from subprocess import check_output


def has_binary(binary):
    return bool(check_output(['which', binary]).strip())


def get_os():
    '''
    passwheel is officially targeted for linux systems.
    This returns "linux" or otherwise.
    '''
    return os.uname().sysname.lower()


def info(s):
    print(s, file=sys.stderr)


def warning(s):
    print('{}{}{}'.format(Fore.YELLOW, s, Fore.RESET), file=sys.stderr)


def error(s):
    print('{}{}{}'.format(Fore.RED, s, Fore.RESET), file=sys.stderr)
