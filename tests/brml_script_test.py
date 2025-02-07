import pytest
import pathlib
import shutil
from pathlib import Path
import sys
sys.path.append('../')
from project_chameleon.brml_converter import brml_converter

def test_brukerbrml_basic_output():
    brukerbrml_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_brukerbrml_basic_output.__name__
        / "test_file.txt"
    )
    assert not brukerbrml_file_path_basic.parent.is_dir()
    brukerbrml_file_path_basic.parent.mkdir()
    try:
        brml_converter('data/bruker/standard.brml', brukerbrml_file_path_basic)
        assert brukerbrml_file_path_basic.is_file()
    finally:
        shutil.rmtree(brukerbrml_file_path_basic.parent)

def test_brukerbrml_output():
    brukerbrml_file_path = (
        pathlib.Path(__file__).parent
        / test_brukerbrml_output.__name__
        / "brml_test_file.txt"
    )
    assert not brukerbrml_file_path.parent.is_dir()
    brukerbrml_file_path.parent.mkdir()
    try:
        brml_converter('data/bruker/standard.brml',brukerbrml_file_path)
        with open(brukerbrml_file_path, 'r') as file:
            test_lines = [file.readline() for _ in range(5)]
        with open('data/bruker/standared_test.txt', 'r') as file:
            base_lines = [file.readline() for _ in range(5)]

        assert test_lines == base_lines
    finally:
        shutil.rmtree(brukerbrml_file_path.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        brml_converter()
    assert str(exc_info.value) =="brukerrawconverter() missing 2 required positional arguments: 'input' and 'output'"