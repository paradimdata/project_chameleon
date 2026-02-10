import pytest
import pathlib
import shutil
import imagehash
from PIL import Image
import sys
sys.path.append('../')
from project_chameleon.jeol_sem_converter import sem_base_plot


def test_jeol_basic_output():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_jeol_basic_output.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    try:
        sem_base_plot('data/jeol_sem/jeol_sem.EMSA',test_file_path)
        assert test_file_path.is_file()
    finally:
        shutil.rmtree(test_file_path.parent)

def test_jeol_sem_hash():
    test_file_path = (
        pathlib.Path(__file__).parent
        / test_jeol_sem_hash.__name__
        / "test_file.png"
    )
    assert not test_file_path.parent.is_dir()
    test_file_path.parent.mkdir()
    sem_base_plot('data/jeol_sem/jeol_sem.EMSA',test_file_path)
    hash0 = imagehash.average_hash(Image.open('data/jeol_sem/jeol_sem.png')) 
    hash1 = imagehash.average_hash(Image.open(test_file_path)) 
    shutil.rmtree(test_file_path.parent)
    assert hash1 - hash0 < 100
    
def test_Jeol_sem_arguments():
    with pytest.raises(TypeError) as exc_info:
        sem_base_plot()
    assert str(exc_info.value) == "sem_base_plot() missing 2 required positional arguments: 'file_name' and 'output_file'"