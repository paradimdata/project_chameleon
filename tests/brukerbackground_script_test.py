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

    # Ensure clean test environment
    if brukerbackground_file_path_basic.parent.exists():
        shutil.rmtree(brukerbackground_file_path_basic.parent)

    brukerbackground_file_path_basic.parent.mkdir(parents=True, exist_ok=True)

    try:
        with patch('builtins.input', return_value=0.15):
            brukerrawbackground(
                'data/bruker/test_background.csv',
                'data/bruker/test_sample.csv',
                brukerbackground_file_path_basic
            )

        assert brukerbackground_file_path_basic.is_dir()

    finally:
        shutil.rmtree(brukerbackground_file_path_basic.parent)


def test_brukerbackground_plot_output():
    brukerbackground_file_path_plot = (
        pathlib.Path(__file__).parent / "test_output"
    )

    # Ensure clean test environment
    if brukerbackground_file_path_plot.exists():
        shutil.rmtree(brukerbackground_file_path_plot)

    brukerbackground_file_path_plot.mkdir(parents=True, exist_ok=True)

    try:
        with patch('builtins.input', return_value=0.85):
            brukerrawbackground(
                'data/bruker/test_background.csv',
                'data/bruker/test_sample.csv',
                brukerbackground_file_path_plot
            )

        expected_output_file = (
            brukerbackground_file_path_plot / "test_output_raw_data.png"
        )

        assert expected_output_file.is_file(), (
            f"Expected output file not found: {expected_output_file}"
        )

    finally:
        shutil.rmtree(brukerbackground_file_path_plot)


import pathlib
import shutil
from unittest.mock import patch

def test_brukerbackground_csv_output():
    brukerbackground_file_path_csv = (
        pathlib.Path(__file__).parent
        / test_brukerbackground_csv_output.__name__
        / "test_file"
    )

    # Ensure test output directory exists
    if not brukerbackground_file_path_csv.exists():
        brukerbackground_file_path_csv.mkdir(parents=True, exist_ok=True)

    try:
        # Run the background subtraction
        with patch("builtins.input", return_value=0.85):
            brukerrawbackground(
                "data/bruker/test_background.csv",
                "data/bruker/test_sample.csv",
                brukerbackground_file_path_csv,
            )

        # Find the generated CSV
        output_files = list(
            brukerbackground_file_path_csv.rglob("*backgroundSubtracted*.csv")
        )
        assert len(output_files) == 1
        output_file = output_files[0]

        # Read the generated CSV (skip header)
        with output_file.open("r") as file:
            next(file)
            generated_lines = [line.strip().split(",")[1:] for line in file]

        # Define baseline CSV path
        baseline_file = (
            pathlib.Path(__file__).parent
            / "test_file"
            / "test_background_subtracted.csv"
        )

        # If baseline doesn't exist, create it from the generated file
        if not baseline_file.exists():
            baseline_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(output_file, baseline_file)

        # Read the baseline CSV (skip header)
        with baseline_file.open("r") as file:
            next(file)
            baseline_lines = [line.strip().split(",")[1:] for line in file]

        # Compare generated CSV with baseline
        assert generated_lines == baseline_lines

    finally:
        # Clean up test output
        if brukerbackground_file_path_csv.parent.exists():
            shutil.rmtree(brukerbackground_file_path_csv.parent)



def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        brukerrawbackground()
    assert str(exc_info.value) =="brukerrawbackground() missing 3 required positional arguments: 'background_input', 'sample_input', and 'output_name'"