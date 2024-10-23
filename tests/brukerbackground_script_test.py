import pytest
import pathlib
import shutil
import numpy as np
from pathlib import Path
from project_chameleon.brukerrawbackground import brukerrawbackground
from unittest.mock import patch

def test_brukerbackground_basic_output():
    brukerbackground_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_basic_output.__name__
        / "test_file.txt"
    )
    assert not brukerbackground_file_path_basic.parent.is_dir()
    brukerbackground_file_path_basic.parent.mkdir()
    try:
        with patch('builtins.input', return_value=.15):
            brukerrawbackground('/project_chameleon/tests/data/bruker/test_background.csv','/project_chameleon/tests/data/bruker/test_sample.csv', 'test_output')
        p = Path('test_output_backgroundSubtracted.csv')
        assert p.is_file()
    finally:
        shutil.rmtree(brukerbackground_file_path_basic.parent)

def test_brukerbackground_plot_output():
    brukerbackground_file_path_plot = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_plot_output.__name__
        / "test_file.txt"
    )
    assert not brukerbackground_file_path_plot.parent.is_dir()
    brukerbackground_file_path_plot.parent.mkdir()
    try:
        with patch('builtins.input', return_value=.85):
            brukerrawbackground('/project_chameleon/tests/data/bruker/test_background.csv','/project_chameleon/tests/data/bruker/test_sample.csv', 'test_output')
        p = Path('test_output_raw_data.png')
        assert p.is_file()
    finally:
        shutil.rmtree(brukerbackground_file_path_plot.parent)

def test_brukerbackground_csv_output():
    brukerbackground_file_path_csv = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_csv_output.__name__
        / "test_file.txt"
    )
    assert not brukerbackground_file_path_csv.parent.is_dir()
    brukerbackground_file_path_csv.parent.mkdir()
    try:
        with patch('builtins.input', return_value=.85):
            brukerrawbackground('/project_chameleon/tests/data/bruker/test_background.csv','/project_chameleon/tests/data/bruker/test_sample.csv', 'test_output')
        with open('test_output_backgroundSubtracted.csv', 'r') as file:
            file.readline()
            for lines in file:
                test_parts = lines.split(',')
                test_line = test_parts[1:]
        with open('test_background_subtracted.csv', 'r') as file:
            file.readline()
            for lines in file:
                base_parts = lines.split(',')
        assert test_line == base_parts
    finally:
        shutil.rmtree(brukerbackground_file_path_csv.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        brukerrawbackground()
    assert str(exc_info.value) =="brukerrawbackground() missing 3 required positional arguments: 'background_input', 'sample_input', and 'output_name'"