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
import subprocess
import re

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

        #Open file as unknown type. Skip header bytes and adjust to a 480 X 640 image. 
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
    

    rheed_video_image_parser(input_file, output_folder = output_file)
    output_name = output_file + output_type
    index = 0
    if output_type == '.avi':
        png_files = sorted(glob.glob(os.path.join(output_file, "*.png")))
        png_files = sorted(png_files, key=lambda s: int(re.findall(r'\d+', s)[-1]) if re.findall(r'\d+', s) else 0)
        
        # Ensure there are matching files
        if not png_files:
            print("No PNG files found in the specified directory.")
        else:
            # Construct the FFmpeg command using the file list
            with open("input_list.txt", "w") as f:
                for file in png_files:
                    f.write(f"file '{file}'\n")
                    f.write(f"duration 0.04\n")
            command = [
                "ffmpeg",
                "-f", "concat",  # Use concat demuxer to concatenate files
                "-safe", "0",    # Allow absolute/relative file paths in the input list
                "-i", "input_list.txt",  # Input list file
                "-framerate", "25",  # Set the frame rate for the output video
                "-f", "avi",   # Output format (avi)
                "-c:v", "rawvideo",  # Video codec
                output_name  # Output file name
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
        png_files = sorted(png_files, key=lambda s: int(re.findall(r'\d+', s)[-1]) if re.findall(r'\d+', s) else 0)
        # Ensure there are matching files
        if not png_files:
            print("No PNG files found in the specified directory.")
        else:
            # Construct the FFmpeg command using the file list
            with open("input_list.txt", "w") as f:
                for file in png_files:
                    f.write(f"file '{file}'\n")
                    f.write(f"duration 0.04\n")
            command = [
                "ffmpeg",
                "-f", "concat",  # Use the concat demuxer
                "-safe", "0",    # Allow absolute paths
                "-i", "input_list.txt",  # Input file containing the list of images and durations
                "-c:v", "libx264",  # Use the libx264 codec
                "-profile:v", "high444",  # Set the H.264 profile
                "-level", "4.0",  # Set the H.264 level
                "-preset", "slow",  # Set the encoding preset
                "-b:v", "3000k",  # Set the video bitrate
                output_name  # Output file name (e.g., output.avi)
            ]
            # Run the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            print("Standard Output:")
            print(stdout)

            if stderr:
                print("Standard Error:")
                print(stderr)
    os.remove('input_list.txt')
    if keep_images == 0:
        shutil.rmtree(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    parser.add_argument("extension", help="output file extension")
    args = parser.parse_args()
    rheed_video_converter(args.input, args.output, args.extension)