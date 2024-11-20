import os
import numpy as np 
from PIL import Image

def get_image_dimensions(input_file):
    with open(input_file,"rb") as f:
        f.seek(39)
        data = f.read(6)
        signature = data.decode('utf-8')
        f.seek(49)
        data = f.read(2)
        width = int.from_bytes(data, byteorder='big') 
        f.seek(321)
        data = f.read(2)
        height = int.from_bytes(data, byteorder='big')
    f.close()
    if signature == 'KSA00F':
        header_size = 640
    elif signature == 'KSA00J':
        header_size = 685
    else:
        raise ValueError("ERROR: Ecountered unknown header.")

    return height, width, header_size

def rheed_video_frame_parser(input_file, height, width, header_bytes):

    with open(input_file,"r") as f:
        f.seek(header_bytes)
        laue = np.fromfile(f,dtype="<u2",count=width*height).reshape((height,width))    
    laue = ((laue/np.max(laue))**(2/3))*255
    laue = laue.astype(np.uint8)
    f.close()
    
    return laue

def rheed_video_image_parser(input_file, output_folder = 'rheed_video_temp'):
    index = 0
    file_size = os.path.getsize(input_file)
    height, width, header_size = get_image_dimensions(input_file)
    cap = int(int(file_size) / (2*(height*width)))
    os.mkdir(output_folder)

    while cap > index:
        header_bytes = header_size + (2*(height*width) + header_size)*index
        file_height = height
        file_width = width

        #Open file as unknown type. Skip header bytes and adjust to a H X W image. 
        with open(input_file,"r") as f:
            f.seek(header_bytes)
            laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_height,file_width))    
        laue = ((laue/np.max(laue))**(2/3))*255
        laue = laue.astype(np.uint8)
        im = Image.fromarray(laue)
        filepath = os.path.join('.', output_folder + '_' + str(index) + '.png')
        im.save(filepath)
        f.close()
        index += 1