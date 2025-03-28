import pytest
import pathlib
import shutil
import os
import imagehash
from PIL import Image
from pathlib import Path
import sys
sys.path.append('../')
from project_chameleon.stemarray4d import stemarray4d

def test_stemarray4d_basic_output():
    stemarray4d_file_path_basic = (
        pathlib.Path(__file__).parent
        / "test_stemarray4d_basic_output"
        / "test_folder"
    )

    # Ensure the directory does not already exist
    assert not stemarray4d_file_path_basic.parent.is_dir()
    stemarray4d_file_path_basic.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Assuming `stemarray4d` is the function being tested
        stemarray4d('data/stemarray4d/stemarray4d_test_data.raw', stemarray4d_file_path_basic)
        
        # Construct the expected output file path
        expected_output_file = stemarray4d_file_path_basic.with_name(stemarray4d_file_path_basic.name + '_max_DP.png')
        
        # Check if the expected output file exists
        assert expected_output_file.is_file(), f"Expected output file not found: {expected_output_file}"
    finally:
        # Clean up by removing the created directory
        shutil.rmtree(stemarray4d_file_path_basic.parent)

def test_stemarray4d_file_output():
    stemarray4d_file_path_file = (
        pathlib.Path(__file__).parent
        / test_stemarray4d_file_output.__name__
        / "test_folder"
    )
    assert not stemarray4d_file_path_file.parent.is_dir()
    stemarray4d_file_path_file.parent.mkdir()
    stemarray4d('data/stemarray4d/stemarray4d_test_data.raw', stemarray4d_file_path_file)
    hash0 = imagehash.average_hash(Image.open('data/stemarray4d/stemarray4d_example__mean_DP.png')) 
    hash1 = imagehash.average_hash(Image.open(Path(str(stemarray4d_file_path_file)+'_mean_DP.png'))) 
    shutil.rmtree(stemarray4d_file_path_file.parent)
    assert hash1 - hash0 < 2

def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        stemarray4d()
    assert str(exc_info.value) == "stemarray4d() missing 2 required positional arguments: 'file_name' and 'output_name'"