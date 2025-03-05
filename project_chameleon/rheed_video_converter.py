import os
import glob
import numpy as np
from PIL import Image
import argparse
import shutil
from sys import argv, exit
from time import time, sleep
from subprocess import Popen, PIPE, DEVNULL
from .rheed_helpers import get_image_dimensions
from .rheed_helpers import rheed_video_frame_parser
from .rheed_helpers import rheed_video_image_parser
import traceback

def rheed_video_converter(input_file, output_file, keep_images = 0):
    """
    ``rheed_video_converter()`` is a function that allows for .imm video files tobe converterd to either .avi(lossless) or .mp4(lossy) video files. This function was written using the package ffmpeg, and it utilizes the functionality of `get_image_dimensions`, `rheed_video_frame_parser`, and `rheed_video_image_parser`. 

    :args: ``file_name`` should be a RHEED .imm file. ``output_file`` is a string which will be the name of the final output file, and should not contain the output extension. ``output_type`` is either '.mp4' or '.avi'. Whichever extension is chosen will be added to the end of ``output_file`` to created the desired output file type. ``keep_images`` is either a 1(keep images) or 0(delete images) to control what to do with images created during the conversion process. This argumnet is optional. 

    :return: this function does not return anything. The output is saved as either a .avi or .mp4 video file. Optionally, a folder containing individual frames as images will also be created. 

    :exception: ``input_file`` must end with '.imm'. ``output_file`` must not contain a file extension. ``output_type`` must be one of the accepted types: '.avi', '.mp4'. ``keep_images`` must be either 1 or 0. 
    """

    # Make sure inputs are the right type
    if not input_file.endswith('.imm'):
        raise ValueError("ERROR: bad input. Expected .imm file")
    if not (output_file.endswith('.avi') or output_file.endswith('.mp4')):
        raise ValueError("ERROR: output_file should should be a .avi or .mp4 file.")
    if not keep_images in [1,0]:
        raise ValueError("ERROR: invalid keep_images value. keep_images may only be a 1(keep) or 0(delete).")
    
    # Initialize variables
    file_size = os.path.getsize(input_file)
    height, width, header_size = get_image_dimensions(input_file)
    cap = file_size // (2 * height * width)
    output_name = output_file 

    if output_file.endswith('.avi'):
        output_type = '.avi'
    elif output_file.endswith('.mp4'):
        output_type = '.mp4'

    # Two output files types: .avi and .mp4. Each have different ffmpeg commands and variables within the command
    if output_type == '.avi':
        ffmpeg = Popen(
        [
            'ffmpeg',
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

        # We need to disect the file as frames, and them as the frames using ffmpeg
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

    # Second type of output file: .mp4
    elif output_type == '.mp4':
        ffmpeg = Popen(
        [
            'ffmpeg',
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

        # We need to disect the file as frames, and them as the frames using ffmpeg
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

    # If the user wants to keep all the images they are all saved here
    if keep_images != 0:
        rheed_video_image_parser(input_file, output_folder = output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    parser.add_argument("extension", help="output file extension")
    args = parser.parse_args()
    rheed_video_converter(args.input, args.output, args.extension)
