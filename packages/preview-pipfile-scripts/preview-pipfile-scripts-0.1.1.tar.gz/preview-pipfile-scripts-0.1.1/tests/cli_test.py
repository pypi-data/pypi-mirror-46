import argparse
import os

import pytest

from pps.cli import arg_parser, main, run_pps_cmd
from pps.message import EXE_SCRIPT_ERR_MSG

from .mock.data import OPT_SHOW_DATA


@pytest.mark.parametrize(
    'arg, namespace', [('--show', argparse.Namespace(show=True))]
)
def test_arg_parser(arg, namespace):
    parser = arg_parser()
    actual = parser.parse_args(arg.split(' '))

    assert actual == namespace


@pytest.mark.parametrize(
    'namespace',
    [argparse.Namespace(show=True), argparse.Namespace(show=False)],
)
def test_run_cmd_pps(namespace):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_name = 'test.toml'
    file_path = '{0}/mock/{1}'.format(root_dir, test_file_name)

    opt, res, err = run_pps_cmd(args=namespace, file_path=file_path, test=True)

    if err == -1:
        pytest.fail(EXE_SCRIPT_ERR_MSG)

    if opt == 'show':
        assert res == [
            'echo: "Echo Hello World!!"',
            'error: "error"',
            'version: "python --version"',
        ]


@pytest.mark.parametrize(
    'namespace',
    [argparse.Namespace(show=True), argparse.Namespace(show=False)],
)
def test_run_cmd_pps_error(namespace):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_name = 'no_script_test.toml'
    invalid_file_path = '{0}/mock/{1}'.format(root_dir, test_file_name)

    with pytest.raises(SystemExit):
        run_pps_cmd(args=namespace, file_path='', test=True)
        run_pps_cmd(args=namespace, file_path=invalid_file_path, test=True)


@pytest.mark.parametrize('arg', ['--show'])
def test_main(arg, capfd):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_name = 'test.toml'
    file_path = '{0}/mock/{1}'.format(root_dir, test_file_name)

    main(arg, file_path)
    out, _ = capfd.readouterr()
    assert out == OPT_SHOW_DATA
