"""
pss provide CLI that preview Pipfile script and run.

$ pps
$ pps --show
"""
import argparse
import os

from .color import CYAN, ENDC
from .helper import (
    exception,
    inquirer_prompt,
    read_file,
    run_script,
    toml_parsing,
)
from .message import EXE_SCRIPT_ERR_MSG


@exception
def run_pps_cmd(args, file_path, test=False):
    """
    Run 'pps' command
    :param args: Arguments to distinguish test or run
    :param file_path: Pipfile path.
    :param test: Argument to distinguish whether it is a test or not.
    :return: opt: CLI option (ex. --show).
             res: Result after run script.
             err: Whether the error occurred.
    """
    scripts = toml_parsing(read_file(file_path))['scripts']

    opt, res, err = None, None, None
    if args.show:
        opt = 'show'
        res = [
            '{0}: "{1}"'.format(script, cmd)
            for script, cmd in sorted(scripts.items())
        ]
    elif not test:
        ans = inquirer_prompt(scripts)
        if ans is None:
            raise KeyboardInterrupt
        cmd = ans['cmd']
        res = run_script(scripts[cmd])
        err = -1 if res != 0 else 1

    return opt, res, err


def arg_parser():
    """
    Create argument parser.
    :return: Parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--show', help="show pipfile scripts list", action='store_true'
    )

    return parser


def main(arg=None, file_path=None):
    """
    Main function to be executed by CLI.
    :param arg: Arguments for testing
    :param file_path: Pipfile path
    """
    parser = arg_parser()
    args = (
        parser.parse_args()
        if arg is None
        else parser.parse_args(arg.split(' '))
    )
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if file_path is None:
        file_path = '{0}/../Pipfile'.format(root_dir)

    opt, res, err = run_pps_cmd(args, file_path)
    if err == -1:
        print(EXE_SCRIPT_ERR_MSG)
        return
    if opt == 'show':
        for cmd_and_script in res:
            cmd, script = cmd_and_script.split(':')
            print('{0}{1}{2}:{3}'.format(CYAN, cmd, ENDC, script))
