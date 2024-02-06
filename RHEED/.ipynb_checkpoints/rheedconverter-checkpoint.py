import os
import numpy as np 
import matplotlib.pyplot as plt
from PIL import image

def rheedconverter(file_name):
    with open(file_name,"r") as f:
        f.seek(685)
        laue = np.fromfile(f,dtype="<u2",count=480*640).reshape((480,640))
    im_temp = laue - laue.min()
    im_temp = im_temp / im_temp.max()
    im_temp = im_temp * 255
    im = Image.fromarray(im_temp.astype(np.uint8))
    im.save("your_file.jpeg")
    return im