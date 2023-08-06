"""
Functions that help the run 'pps' command
"""
import functools
import subprocess

import inquirer
import toml

from .message import (
    FILE_NOT_FOUND_MSG,
    INQUIRER_MSG,
    KEYBOARD_INTERRUPT_MSG,
    KEYWORD_NOT_FOUND_MSG,
)


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            print(KEYWORD_NOT_FOUND_MSG)
            exit()
        except FileNotFoundError:
            print(FILE_NOT_FOUND_MSG)
            exit()
        except KeyboardInterrupt:
            print(KEYBOARD_INTERRUPT_MSG)
            exit()

    return wrapper


def read_file(file_path):
    """
    Read file
    :param file_path: File path
    :return: File content
    """
    reader = open(file_path, 'r', encoding="utf8")
    file_content = reader.read()
    reader.close()

    return file_content


def toml_parsing(toml_string):
    """
    Parses the "toml" string and return dictionary format
    :param toml_string: String that is a "toml" file format.
    :return: Return dictionary format
    """
    parsed_toml = toml.loads(toml_string)

    return parsed_toml


def inquirer_prompt(choice):
    """
    Return selected results from choices.
    :param choice: choices
    :return: Return selected result
    """
    questions = [inquirer.List('cmd', message=INQUIRER_MSG, choices=choice)]
    answer = inquirer.prompt(questions)
    return answer


def run_script(script):
    """
    Run the script.
    :param script: Script to run.
    :return: The result of the script execution.
    """
    p_ret_code = subprocess.call(script, shell=True)

    return p_ret_code
