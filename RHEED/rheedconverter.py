import os
import numpy as np 
import matplotlib.pyplot as plt
from PIL import image
header_bytes = 685
file_width = 480
file_height = 640

def rheedconverter(file_name):

    #Open file as unknown type. Skip header bytes and adjust to a 480 X 640 image. 
    with open(file_name,"r") as f:
        f.seek(header_bytes)
        laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_width,file_height))
    
    #Operate to adjust from 16bpp to 8 bpp so the image can be displayed easier
    im_temp = laue - laue.min()
    im_temp = im_temp / im_temp.max()
    im_temp = im_temp * 255
   
    #Adjust to unsigned integers and save as a jpeg
    im = Image.fromarray(im_temp.astype(np.uint8))
    im.save("your_file.jpeg")
    