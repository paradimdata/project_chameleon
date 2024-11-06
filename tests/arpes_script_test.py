import pytest
import pathlib
import shutil
import numpy as np
from pathlib import Path
import pandas as pd
import sys
sys.path.append('../')
from project_chameleon.arpes import arpes_folder_workbook
from unittest.mock import patch

def test_arpes_basic_output():
    arpes_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_arpes_basic_output.__name__
        / "test_output.xlsx"
    )
    assert not arpes_file_path_basic.parent.is_dir()
    arpes_file_path_basic.parent.mkdir()
    try:
        arpes_folder_workbook('data/arpes/ARPES_test_folder/ARPES Raw Data/NbO/Al2O3_0001/JF24020', arpes_file_path_basic)
        assert arpes_file_path_basic.is_file()
    finally:
        shutil.rmtree(arpes_file_path_basic.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        arpes_folder_workbook()
    assert str(exc_info.value) =="arpes_folder_workbook() missing 2 required positional arguments: 'folder_name' and 'workbook_name'"