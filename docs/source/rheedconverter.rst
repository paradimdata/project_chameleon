==========================================
RHEED Video and Image Processing Functions
==========================================

This module contains several functions for handling RHEED (Reflection High-Energy Electron Diffraction) video and image files. The primary function of the module is to read raw data from RHEED `.imm` and `.img` files, process the data, and convert it into more usable formats like `.avi`, `.mp4`, and `.png`.

The module includes the following functions:

- ``get_image_dimensions(input_file)``: Extracts the image dimensions (height, width, and header size) from a RHEED `.imm` file.
- ``rheed_video_frame_parser(input_file, height, width, header_bytes)``: Reads and processes a single frame from a RHEED video file.
- ``rheed_video_image_parser(input_file, output_folder='rheed_video_temp')``: Parses the video file and saves each frame as an individual image in a specified folder.
- ``rheed_video_converter(input_file, output_file, output_type, keep_images=0)``: Converts a RHEED `.imm` video file into either an `.avi` (lossless) or `.mp4` (lossy) video file, with an option to keep or delete the individual images generated during the conversion.
- ``rheedconverter(file_name, output_file)``: Converts a 16-bit `.img` RHEED image file into an 8-bit `.png` image file for easier viewing.

The functions support the following arguments:

- ``input_file``: The path to the `.imm` or `.img` file to process.
- ``output_file``: The name of the output video or image file (without extension).
- ``output_type``: For video conversion, either `'.avi'` or `'.mp4'` to specify the output format.
- ``keep_images``: A flag (1 to keep, 0 to delete) indicating whether to keep the images generated during video conversion (default is `0`).
- ``output_folder``: The folder where the frames will be saved during video conversion (default is `'rheed_video_temp'`).
- ``folder_name``: The directory path containing the scan files (for other use cases not present in the functions).

Please note that if the input file is not the expected file type or if an invalid file extension or argument is passed, exceptions will be raised.

.. automodule:: rheed_video_processing
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main