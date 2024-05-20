import pytest
import pathlib
import shutil
from pathlib import Path
from XRD.BrukerRAW.brukerrawconverter import brukerrawconverter

def test_brukerraw_basic_output():
    brukerraw_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_brukerraw_basic_output.__name__
        / "test_file.txt"
    )
    assert not brukerraw_file_path_basic.parent.is_dir()
    brukerraw_file_path_basic.parent.mkdir()
    try:
        brukerrawconverter('/data/bruker/brukerraw_test.RAW',brukerraw_file_path_basic)
        assert brukerraw_file_path_basic.is_file()
    finally:
        shutil.rmtree(brukerraw_file_path_basic.parent)

def test_brukerraw_output():
    brukerraw_file_path = (
        pathlib.Path(__file__).parent
        / test_brukerraw_output.__name__
        / "probe_test_file.txt"
    )
    assert not brukerraw_file_path.parent.is_dir()
    brukerraw_file_path.parent.mkdir()
    try:
        brukerrawconverter('/data/bruker/brukerraw_test.RAW',brukerraw_file_path)
        with open(brukerraw_file_path, 'r') as file:
            test_lines = [file.readline() for _ in range(5)]
        with open('bruker_output.txt', 'r') as file:
            base_lines = [file.readline() for _ in range(5)]

        assert test_lines == base_lines
    finally:
        shutil.rmtree(brukerraw_file_path.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        brukerrawconverter()
    assert str(exc_info.value) =="brukerrawconverter() missing 2 required positional arguments: 'input_file' and 'output_file'"