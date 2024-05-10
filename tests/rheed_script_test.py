import pytest
import pathlib
import shutil
import imagehash
from PIL import Image
from rheedconverter import main
from rheedconverter import rheedconverter


def test_rheed_basic_output():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_rheed_hash.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    try:
        rheedconverter('test.img',test_file_path)
        assert test_file_path.is_file()
    finally:
        shutil.rmtree(test_file_path.parent)

def test_rheed_hash():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_rheed_hash.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    rheedconverter('test.img',test_file_path)
    hash0 = imagehash.average_hash(Image.open('new_test_output.png')) 
    hash1 = imagehash.average_hash(Image.open(test_file_path)) 
    shutil.rmtree(test_file_path.parent)
    assert hash1 - hash0 < 5
    
def test_no_arguments():
    with pytest.raises(TypeError) as exc_info:
        rheedconverter()
    assert str(exc_info.value) == "rheedconverter() missing 2 required positional arguments: 'file_name' and 'output_file'"