import pytest
import pathlib
import shutil
import os
from pathlib import Path
import sys
sys.path.append('../')
from project_chameleon.non4dstem import non4dstem

def test_non4dstem_basic_folder_output():
    non4dstem_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_non4dstem_basic_folder_output.__name__
        / "test_folder"
    )
    assert not non4dstem_file_path_basic.parent.is_dir()
    non4dstem_file_path_basic.parent.mkdir()
    try:
        non4dstem(data_folder = 'data/non4dstem_data', outputs_folder = non4dstem_file_path_basic)
        assert non4dstem_file_path_basic.is_dir()
    finally:
        shutil.rmtree(non4dstem_file_path_basic.parent)

def test_non4dstem_basic_file_output():
    non4dstem_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_non4dstem_basic_file_output.__name__
        / "test_file.png"
    )
    assert not non4dstem_file_path_basic.parent.is_dir()
    non4dstem_file_path_basic.parent.mkdir()
    try:
        non4dstem(data_file = 'data/non4dstem_data/005_ADF Image (SI Survey).dm4', output_file = non4dstem_file_path_basic)
        assert non4dstem_file_path_basic.is_file()
    finally:
        shutil.rmtree(non4dstem_file_path_basic.parent)

def test_non4dstem_file_output():
    non4dstem_file_path_file = (
        pathlib.Path(__file__).parent
        / test_non4dstem_file_output.__name__
        / "test_folder"
    )
    assert not non4dstem_file_path_file.parent.is_dir()
    non4dstem_file_path_file.parent.mkdir()
    try:
        non4dstem(data_folder = 'data/non4dstem_data', outputs_folder = non4dstem_file_path_file)
        files = os.listdir(non4dstem_file_path_file)
        assert files

    finally:
        shutil.rmtree(non4dstem_file_path_file.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        non4dstem()
    assert str(exc_info.value) =="non4dstem() missing 2 required positional arguments: 'data_folder' and 'outputs_folder'"