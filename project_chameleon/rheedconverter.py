import os
import numpy as np 
import matplotlib.pyplot as plt
import sys
import argparse

def rheedconverter(file_name, output_file):
    """
    ``rheedconverter()`` is a function to allow RHEED users to convert 16 bpp .img images into 8 bpp more easily readable .jpeg images

    :args: This function has two inputs: ``file_name`` and ``output_file``. ``file_name`` should be a rheed .img file. This function has been designed to handle images with dimensions of 1024x1024 as that is the standard size for RHEED images used for developing this function. ``output_file`` is a string which will be the name of the final output file. 

    :return: this function does not return anything. The output is saved as an image file.

    :exception: will throw an exception if the input file is not a .img file.
    """

    #Make sure input is a .img file
    if not file_name.endswith('.img'):
        raise ValueError("ERROR: bad input. Expected .img file")
    
    file_size = os.path.getsize(file_name)
    if file_size < 1000000:
        if file_size == 615040:
            header_bytes = 320
            file_width = 480
            file_height = 640
        else:
            header_bytes = 685
            file_width = 480
            file_height = 640
    else:
        header_bytes = 640
        file_width = 1024
        file_height = 1024
    
    #Open file as unknown type. Skip header bytes and adjust to a 480 X 640 image. 
    with open(file_name,"r") as f:
        f.seek(header_bytes)
        laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_width,file_height))
    
    #Operate to adjust from 16bpp to 8 bpp so the image can be displayed easier
    im_temp = laue - laue.min()
    im_temp = im_temp / im_temp.max()
    im_temp = im_temp * 255
   
    #Adjust to unsigned integers and save as a jpeg
    im_uint8_scaled = im_temp.astype(np.uint8)
    plt.axis('off')
    plt.imshow(im_uint8_scaled)
    plt.savefig(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    rheedconverter(args.input, args.output)