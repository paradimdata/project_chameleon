import pytest
import pathlib
import shutil
import numpy as np
from pathlib import Path
import sys
sys.path.append('../')
from project_chameleon.brukerrawbackground import brukerrawbackground
from unittest.mock import patch

def test_brukerbackground_basic_output():
    brukerbackground_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_basic_output.__name__
        / "test_output"
    )
    assert not brukerbackground_file_path_basic.parent.is_dir()
    brukerbackground_file_path_basic.parent.mkdir()
    try:
        with patch('builtins.input', return_value=.15):
            brukerrawbackground('data/bruker/test_background.csv','data/bruker/test_sample.csv', brukerbackground_file_path_basic)
        assert brukerbackground_file_path_basic.is_dir()
    finally:
        shutil.rmtree(brukerbackground_file_path_basic.parent)

def test_brukerbackground_plot_output():
    brukerbackground_file_path_plot = (
        pathlib.Path(__file__).parent
        / "test_output"
    )

    # Ensure a clean test environment
    if brukerbackground_file_path_plot.is_dir():
        shutil.rmtree(brukerbackground_file_path_plot)
    #brukerbackground_file_path_plot.mkdir(parents=True, exist_ok=True)
    
    try:
        # Mock input and run the function
        with patch('builtins.input', return_value=0.85):
            brukerrawbackground(
                'data/bruker/test_background.csv',
                'data/bruker/test_sample.csv',
                brukerbackground_file_path_plot
            )
        
        # Define expected output file path
        expected_output_file = brukerbackground_file_path_plot / "test_output_raw_data.png"

        # Check if the expected output file exists
        assert expected_output_file.is_file(), f"Expected output file not found: {expected_output_file}"

    finally:
        # Clean up test output directory
        shutil.rmtree(brukerbackground_file_path_plot)

def test_brukerbackground_csv_output():
    brukerbackground_file_path_csv = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_csv_output.__name__
        / "test_file"
    )
    assert not brukerbackground_file_path_csv.parent.is_dir()
    try:
        with patch('builtins.input', return_value=.85):
            brukerrawbackground('data/bruker/test_background.csv','data/bruker/test_sample.csv', brukerbackground_file_path_csv)
        with open(str(brukerbackground_file_path_csv) + '/test_output_backgroundSubtracted.csv', 'r') as file:
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