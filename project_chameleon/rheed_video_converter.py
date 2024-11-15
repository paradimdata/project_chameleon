import os
import glob
import numpy as np 
from PIL import Image
import argparse
import shutil
from sys import argv, exit
from lz4.frame import decompress
from time import time, sleep
from subprocess import Popen, PIPE, DEVNULL
import subprocess

def rheed_video_image_parser(input_file, output_file = 'rheed_video_temp'):
    index = 0
    file_size = os.path.getsize(input_file)
    cap = int(int(file_size) / (2*(1024*1024)))
    os.mkdir(output_file)

    while cap > index:
        header_bytes = 640 + (2*(1024*1024) + 640)*index
        file_height = 1024
        file_width = 1024

        #Open file as unknown type. Skip header bytes and adjust to a 480 X 640 image. 
        with open(input_file,"r") as f:
            f.seek(header_bytes)
            laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_width,file_height))    
        laue = ((laue/np.max(laue))**(2/3))*255
        laue = 255 - laue
        laue = laue.astype(np.uint8)
        im = Image.fromarray(laue)
        im.save(output_file + str(index) + '.png')
        filepath = os.path.join('.', 'test' + str(index) + '.png')
        shutil.move(filepath, os.path.join(output_file, output_file + str(index) + '.png'))
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
    if not '.avi' or '.mp4' in output_type:
        raise ValueError("ERROR: invalid output type. Output type must be either .avi or .mp4.")
    if not 1 or 0 in keep_images:
        raise ValueError("ERROR: invalid keep_images value. keep_images may only be a 1(keep) or 0(delete).")
    

    rheed_video_image_parser(input_file, output_file)
    output_name = output_file + output_type
    if output_type == '.avi':
        png_files = sorted(glob.glob(os.path.join(output_file, "*.png")))
        # Ensure there are matching files
        if not png_files:
            print("No PNG files found in the specified directory.")
        else:
            # Construct the FFmpeg command using the file list
            input_pattern = os.path.join(output_file, "*.png")
            command = [
                "ffmpeg",
                "-framerate", "25",
                "-pattern_type", "glob",
                "-i", input_pattern,
                "-f", "avi",
                "-c:v", "rawvideo",
                output_name
            ]
            # Run the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            print("Standard Output:")
            print(stdout)

            if stderr:
                print("Standard Error:")
                print(stderr)
    elif output_type == '.mp4':
        png_files = sorted(glob.glob(os.path.join(output_file, "*.png")))
        # Ensure there are matching files
        if not png_files:
            print("No PNG files found in the specified directory.")
        else:
            # Construct the FFmpeg command using the file list
            input_pattern = os.path.join(output_file, "*.png")
            command = [
                "ffmpeg",
                "-framerate", "25",
                "-pattern_type", "glob",
                "-i", input_pattern,
                "-c:v", "libx264",
                "-profile:v", "high444",
                "-level", "4.0",
                "-preset", "slow",
                "-b:v", "3000k",
                output_name
            ]
            # Run the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            print("Standard Output:")
            print(stdout)

            if stderr:
                print("Standard Error:")
                print(stderr)

    if keep_images == 0:
        shutil.rmtree('rheed_video_temp')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    parser.add_argument("extension", help="output file extension")
    args = parser.parse_args()
    rheed_video_converter(args.input, args.output, args.extension)