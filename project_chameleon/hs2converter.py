import numpy as np 
import os
import matplotlib.pyplot as plt
from PIL import Image
import argparse

def hs2converter(file_name, output_file):
    """
    ``hs2converter()`` is a function to allow users to convert a difficult to handle 16bpp hs2 to an easily readable 8bpp png image.

    :args: This function has two inputs: ``file_name`` and ``output_file``. ``file_name`` should be a .hs2 file. ``output_file`` should be a string which will be the name of the output .png file. 

    :return: this function does not return anything. The output is saved as an image file.

    :exception: will throw an exception if the input file is not a .hs2 file, or if the input file does not exist.
    """

    #Make sure input is a .img file
    if not str(file_name).endswith('.hs2'):
        raise ValueError("ERROR: bad input. Expected .hs2 file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    if not os.path.isfile(file_name):
        raise ValueError("ERROR: Input should be a file. Check if your file exists.")

    file_size = os.path.getsize(file_name)

    if file_size < 530424:
        #Set file size
        file_width = 256
        file_height = 256
    else:
        file_width = 512
        file_height = 512

    #Read data from file, little endian. Once data is read, invert it, create an image, rotate the image 90 degrees, and save the image
    with open(file_name,"r") as f:
            laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_width,file_height))       
    laue = ((laue/np.max(laue))**(2/3))*255
    laue = 255 - laue
    laue = laue.astype(np.uint8)
    im = Image.fromarray(laue)
    im = im.rotate(90)
    im.save(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    hs2converter(args.input, args.output)
