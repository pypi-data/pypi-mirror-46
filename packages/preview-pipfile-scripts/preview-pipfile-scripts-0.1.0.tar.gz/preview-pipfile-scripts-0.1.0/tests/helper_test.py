import os

from pps.helper import read_file, run_script, toml_parsing

from .mock.data import INPUT_TOML_DATA, OUTPUT_TOML_DATA


def test_read_file():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_name = 'test.txt'
    file_path = '{0}/mock/{1}'.format(root_dir, test_file_name)

    res = read_file(file_path)
    assert res == 'hello read file txt'


def test_toml_parsing():
    res = toml_parsing(INPUT_TOML_DATA)
    assert res == OUTPUT_TOML_DATA


def test_run_script():
    res = run_script('python --version')
    assert res == 0
