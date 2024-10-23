import pytest
import pathlib
import shutil
import numpy as np
from pathlib import Path
from project_chameleon.arpes import arpes_folder_workbook
from unittest.mock import patch

def test_arpes_basic_output():
    arpes_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_arpes_basic_output.__name__
        / "test_file.txt"
    )
    assert not arpes_file_path_basic.parent.is_dir()
    arpes_file_path_basic.parent.mkdir()
    try:
        with patch('builtins.input', return_value=.15):
            arpes_folder_workbook('/project_chameleon/tests/data/arpes/PARADIM 290 - Falson - NbO/ARPES Raw Data/Al2O3_0001/JF24020', 'test_output.xlsx')
        p = Path('test_file.xlsx')
        assert p.is_file()
    finally:
        shutil.rmtree(arpes_file_path_basic.parent)

def test_arpes_xlsx_output():
    arpes_file_path_xlsx = (
        pathlib.Path(__file__).parent
        / test_arpes_xlsx_output.__name__
        / "test_file.txt"
    )
    assert not arpes_file_path_xlsx.parent.is_dir()
    arpes_file_path_xlsx.parent.mkdir()
    try:
        arpes_folder_workbook('/project_chameleon/tests/data/arpes/PARADIM 290 - Falson - NbO/ARPES Raw Data/Al2O3_0001/JF24020','test_output.xlsx')
        with open('test_output.xslx', 'r') as file:
            file.readline()
            for lines in file:
                test_line = lines
        with open('/project_chameleon/tests/data/arpes/JF24020.xlsx', 'r') as file:
            file.readline()
            for lines in file:
                base_parts = lines
        assert test_line == base_parts
    finally:
        shutil.rmtree(arpes_file_path_xlsx.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        arpes_folder_workbook()
    assert str(exc_info.value) =="arpes_folder_workbook() missing 2 required positional arguments: 'folder_name' and 'workbook_name'"