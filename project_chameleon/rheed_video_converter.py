import os
import glob
import numpy as np 
from PIL import Image
import argparse
import shutil
from sys import argv, exit
from time import time, sleep
from subprocess import Popen, PIPE, DEVNULL
from get_image_dimensions import get_image_dimensions
import traceback

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
        index += 1

def rheed_video_converter(input_file, output_file, output_type, keep_images = 0):
    """
    ``rheed_video_converter()`` is a function to allow RHEED users to convert .imm video files to either .avi(lossless) or .mp4(lossy) video files.

    :args: This function has four inputs: ``input_file``, ``output_file``, ``output_type``, and ``keep_images``. ``file_name`` should be a RHEED .imm file. This function has been designed to handle images with dimensions of 1024x1024 as that is the standard size for RHEED images used for developing this function. ``output_file`` is a string which will be the name of the final output file. ``output_file`` should not contain the desired file extension. ``output_type`` is either '.mp4' or '.avi'. Whichever extension is chosen will be added to the end of ``output_file`` to created the desired output file type. ``keep_images`` is either a 1(keep images) or 0(delete images) to control what to do with images created during the conversion process.

    :return: this function does not return anything. The output is saved as either a .avi or .mp4 video file.

    :exception: will throw an exception if the input file is not a .imm file, if the output type is not correct, if the output file has a file extension, or if the value in keep_images is not 1 or 0.
    """

    if not input_file.endswith('.imm'):
        raise ValueError("ERROR: bad input. Expected .imm file")
    if output_file.endswith('.avi') or output_file.endswith('.mp4'):
        raise ValueError("ERROR: output_file should not contain file extension, just file name.")
    if not output_type in ['.avi','.mp4']:
        raise ValueError("ERROR: invalid output type. Output type must be either .avi or .mp4.")
    if not keep_images in [1,0]:
        raise ValueError("ERROR: invalid keep_images value. keep_images may only be a 1(keep) or 0(delete).")
    
    file_size = os.path.getsize(input_file)
    height, width, header_size = get_image_dimensions(input_file)
    print(height, width, header_size)
    cap = file_size // (2 * height * width)
    output_name = output_file + output_type
    if output_type == '.avi':
        ffmpeg = Popen(
        [
            '/opt/homebrew/bin/ffmpeg',
            '-f', 'rawvideo',  # Input format is raw video
            '-pixel_format', 'gray',  # Pixel format
            '-video_size', f'{width}x{height}',  # Frame dimensions
            '-framerate', '25',  # Frame rate
            '-i', 'pipe:0',  # Input via stdin
            "-f", "avi",   # Output format (avi)
            "-c:v", "rawvideo",
            output_name,  # Output file
        ],
        stdin=PIPE,
        stdout=DEVNULL,
        stderr=DEVNULL
        )

        try:
            for index in range(cap):
                additional_header = (2 * height * width + header_size) * index
                try:
                    frame_data = rheed_video_frame_parser(input_file, height, width, header_size + additional_header)
                    ffmpeg.stdin.write(frame_data)
                except Exception as e:
                    traceback.print_exc()
        finally:
            # Properly close FFmpeg and wait for it to finish
            ffmpeg.stdin.close()
            ffmpeg.wait()

    elif output_type == '.mp4':
        ffmpeg = Popen(
        [
            '/opt/homebrew/bin/ffmpeg',
            '-f', 'rawvideo',  # Input format is raw video
            '-pixel_format', 'gray',  # Pixel format
            '-video_size', f'{width}x{height}',  # Frame dimensions
            '-framerate', '25',  # Frame rate
            '-i', 'pipe:0',  # Input via stdin
            '-c:v', 'libx264',  # Use the H.264 codec
            '-profile:v', 'high444',  # H.264 profile
            '-level', '4.0',  # H.264 level
            '-preset', 'slow',  # Encoding preset
            '-b:v', '3000k',  # Bitrate
            '-y',  # Overwrite output file
            output_name,  # Output file
        ],
        stdin=PIPE,
        stdout=DEVNULL,
        stderr=DEVNULL
        )

        try:
            for index in range(cap):
                additional_header = (2 * height * width + header_size) * index
                try:
                    frame_data = rheed_video_frame_parser(input_file, height, width, header_size + additional_header)
                    ffmpeg.stdin.write(frame_data)
                except Exception as e:
                    traceback.print_exc()
        finally:
            # Properly close FFmpeg and wait for it to finish
            ffmpeg.stdin.close()
            ffmpeg.wait()

    if keep_images != 0:
        rheed_video_image_parser(input_file, output_folder = output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    parser.add_argument("extension", help="output file extension")
    args = parser.parse_args()
    rheed_video_converter(args.input, args.output, args.extension)