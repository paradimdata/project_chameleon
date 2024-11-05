import pytest
import pathlib
import shutil
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.append('../')
from project_chameleon.mbeparser import mbeparser
from project_chameleon.mbeparser import find_shutter_values


def test_shutter_values():
    shutter_array = find_shutter_values(36)
    assert shutter_array == [6,3]

def test_mbe_basic_output():
    test_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_mbe_basic_output.__name__
        / "test_folder"
    )
    assert not test_file_path_basic.parent.is_dir()
    test_file_path_basic.parent.mkdir()
    shutil.copytree('data/mbe/mbe_test_data', test_file_path_basic)
    try:
        assert test_file_path_basic.is_dir()
    finally:
        shutil.rmtree(test_file_path_basic.parent)

def test_mbe_folders_useful():
    test_file_path_folders_useful = (
        pathlib.Path(__file__).parent
        / test_mbe_folders_useful.__name__
        / "test_folder"
    )
    assert not test_file_path_folders_useful.parent.is_dir()
    test_file_path_folders_useful.parent.mkdir()
    try:
        shutil.copytree('data/mbe/mbe_test_data', test_file_path_folders_useful)
        with patch('builtins.input', return_value='4'):
            mbeparser(test_file_path_folders_useful)
        useful_path = Path(str(test_file_path_folders_useful) + '/useful')
        assert useful_path.is_dir()
    finally:
        shutil.rmtree(test_file_path_folders_useful.parent)

def test_mbe_folders_useless():
    test_file_path_folders_useless = (
        pathlib.Path(__file__).parent
        / test_mbe_folders_useless.__name__
        / "test_folder"
    )
    assert not test_file_path_folders_useless.parent.is_dir()
    test_file_path_folders_useless.parent.mkdir()
    try:
        shutil.copytree('project_chameleon/tests/data/mbe/mbe_test_data', test_file_path_folders_useless)
        with patch('builtins.input', return_value='4'):
            mbeparser(test_file_path_folders_useless)
        useful_path = Path(str(test_file_path_folders_useless) + '/useless')
        assert useful_path.is_dir()
    finally:
        shutil.rmtree(test_file_path_folders_useless.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        mbeparser()
    assert str(exc_info.value) =="mbeparser() missing 1 required positional argument: 'file_folder'"