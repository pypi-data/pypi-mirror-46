"""
messages
"""
from .color import ENDC, FAIL, OKBLUE, YELLOW

EXE_SCRIPT_ERR_MSG = '{0}[!]{1} An error occurred while executing script in Pipfile'.format(
    FAIL, ENDC
)
KEYWORD_NOT_FOUND_MSG = "{0}[!]{1} {2}Pipfile{1} in {3}[scripts]{1} keyword not found!".format(
    FAIL, ENDC, OKBLUE, YELLOW
)
FILE_NOT_FOUND_MSG = "{0}[!]{1} {2}Pipfile{1} not found!".format(
    FAIL, ENDC, OKBLUE
)
KEYBOARD_INTERRUPT_MSG = "{0}[!]{1} KeyboardInterrupt".format(FAIL, ENDC)
INQUIRER_MSG = "{0}Select Pipfile script to run{1}".format(YELLOW, ENDC)
