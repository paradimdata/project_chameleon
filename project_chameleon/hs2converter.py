import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import argparse

def hs2converter(file_name, output_file):
    """
    ``hs2converter()`` is a function that converts 16bpp hs2 images to 8bpp png image. This image is modified slightly from its original form so patterns in the data are easier to distinguish.

    :args: ``file_name`` should be a .hs2 file. ``output_file`` should be a string which will be the name of the output .png file. 

    :return: this function does not return anything. The output is saved as an image file.

    :exception: `file_name` must be an .hs2 file. `file_name` must be a file. `output_file` must end with '.png'.
    """

    #Make sure input is a .img file
    if not str(file_name).endswith('.hs2'):
        raise ValueError("ERROR: bad input. Expected .hs2 file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    if not os.path.isfile(file_name):
        raise ValueError("ERROR: Input should be a file. Check if your file exists.")

    file_size = os.path.getsize(file_name)

    # Set file dimensions based on file size so dimensions can be applied correctly when the array is reshaped
    if file_size < 530424:
        file_width = 256
        file_height = 256
    else:
        file_width = 512
        file_height = 512

    #Read data from file, little endian. Reshape image to an array of image dimension size
    with open(file_name,"r") as f:
            laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_width,file_height))     

    # Apply gamma filtering to data. 2/3 showed best results in testing. Other values could work better for other purposes  
    laue = ((laue/np.max(laue))**(2/3))*255
    laue = 255 - laue # Invert black and white
    laue = laue.astype(np.uint8) # Change from 16 bit to 8 bit
    im = Image.fromarray(laue) # Create image using PIL
    im = im.rotate(90) # Rotate 90, expected image is rotated 90 degrees
    im.save(output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    hs2converter(args.input, args.output)
