import pytest
import pathlib
import shutil
import imagehash
from PIL import Image
from project_chameleon.hs2converter import hs2converter


def test_hs2_basic_output():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_hs2_basic_output.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    try:
        hs2converter('/project_chameleon/tests/data/rheed/test.hs2',test_file_path)
        assert test_file_path.is_file()
    finally:
        shutil.rmtree(test_file_path.parent)

def test_hs2_hash():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_hs2_hash.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    hs2converter('/project_chameleon/tests/data/rheed/test.hs2',test_file_path)
    hash0 = imagehash.average_hash(Image.open('hs2.png')) 
    hash1 = imagehash.average_hash(Image.open(test_file_path)) 
    shutil.rmtree(test_file_path.parent)
    assert hash1 - hash0 < 5
    
def test_hs2_arguments():
    with pytest.raises(TypeError) as exc_info:
        hs2converter()
    assert str(exc_info.value) == "rheedconverter() missing 2 required positional arguments: 'file_name' and 'output_file'"