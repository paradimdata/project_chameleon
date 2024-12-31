import os
import numpy as np 
import argparse
from PIL import Image
from rheed_helpers import get_image_dimensions


def rheedconverter(file_name, output_file):
    """
    ``rheedconverter()`` is a function that converts 16 bpp .img images into 8 bpp .png images. This function distiguishes image size based on headers in the data. If your file is of a different type than the files on which this function was tested, this function may not work correctly. This function utilizes the functionality of `get_image_dimensions`.

    :args: ``file_name`` should be a string or path to a RHEED file ending in '.img'. ``output_file`` is a string which will be the name of the final output file, which should end with '.png'. 

    :return: this function does not return anything. The output is saved as an .png image file.

    :exception: `input_file` must end with '.img'. `output_file` must end with '.png'. 
    """

    #Make sure input is a .img file
    if not file_name.endswith('.img'):
        raise ValueError("ERROR: bad input. Expected .img file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    
    # Initialize values using helper function
    file_height, file_width, header_bytes = get_image_dimensions(file_name)
    
    #Open file as unknown type. Skip header bytes and adjust to a height X width image. 
    with open(file_name,"r") as f:
        f.seek(header_bytes)
        if header_bytes == 5120: # Hard coded scenario for single crystal .img files
            laue = np.fromfile(f,dtype=np.uint8,count=512*512).reshape((512,512))
        else:
            laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_height,file_width))
    
    #Operate to adjust from 16bpp to 8 bpp so the image can be displayed easier
    laue = ((laue/np.max(laue))**(2/3))*255
    laue = laue.astype(np.uint8)
    im = Image.fromarray(laue) # Use PIL to create image
    if header_bytes == 5120:
        im = im.rotate(90)
    im.save(output_file)
 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    rheedconverter(args.input, args.output)