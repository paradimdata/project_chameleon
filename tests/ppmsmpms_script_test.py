import pytest
import pathlib
import shutil
from pathlib import Path
from unittest.mock import patch
from ppmsmpms.ppmsmpms import ppmsmpmsparser


def test_ppms_basic_output():
    ppms_file_path_basic = (
        pathlib.Path(__file__).parent
        / test_ppms_basic_output.__name__
        / "test_file.txt"
    )
    assert not ppms_file_path_basic.parent.is_dir()
    ppms_file_path_basic.parent.mkdir()
    try:
        with patch('builtins.input', return_value="4-Probe Resistivity"):
            ppmsmpmsparser('/project_chameleon/tests/data/ppms/4-probe resistivity example file.dat', ppms_file_path_basic)
        assert ppms_file_path_basic.is_file()
    finally:
        shutil.rmtree(ppms_file_path_basic.parent)

def test_ppms_probe_output():
    ppms_file_path_probe = (
        pathlib.Path(__file__).parent
        / test_ppms_probe_output.__name__
        / "probe_test_file.txt"
    )
    assert not ppms_file_path_probe.parent.is_dir()
    ppms_file_path_probe.parent.mkdir()
    try:
        with patch('builtins.input', return_value="4-Probe Resistivity"):
            ppmsmpmsparser('/project_chameleon/tests/data/ppms/4-probe resistivity example file.dat', ppms_file_path_probe)
        with open(ppms_file_path_probe, 'r') as file:
            test_lines = [file.readline() for _ in range(5)]
        with open('probe_test_output.txt', 'r') as file:
            base_lines = [file.readline() for _ in range(5)]

        assert test_lines == base_lines
    finally:
        shutil.rmtree(ppms_file_path_probe.parent)

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        ppmsmpmsparser()
    assert str(exc_info.value) =="ppmsmpmsparser() missing 2 required positional arguments: 'inputfile' and 'outputfile'"