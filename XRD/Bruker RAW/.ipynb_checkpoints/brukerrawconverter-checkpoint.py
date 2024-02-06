import os
import xylib

def brukerrawconverter(file_name):
    full_name = file_name + '.RAW'
    csv_name = file_name + '.txt'
    file_size = os.path.getsize(full_name)
    %run xyconv.py full_name csv_name