============================================
Reflection High-Energy Electron Diffraction
============================================

This module contains functions for Reflection High-Energy Electron Diffraction (RHEED) data. These functions primarily convert two file types: RHEED `.img` image files and RHEED `.imm` video files. The ``rheedconverter`` function also supports Crysalis Pro Single Crystal diffraction `.img` images. The two main functions in this module are ``rheedconverter`` and ``rheed_video_converter``. Other functions serve as helpers for these two.

Both main functions perform the same core task: converting 16bpp images or videos to 8bpp. This can be helpful when working with RHEED data, as 16bpp files are not easily viewable on most standard systems. Some functions in this module rely on specific headers found in the original file formats. If your data does not include these headers, the functions may not work correctly.

RHEED Image Converter 
---------------------
``rheedconverter`` takes a RHEED `.img` file as input, extracts all image data, and converts it into a `.png` file. Here is an example of how the function ``rheedconverter`` can be used:

.. code-block:: python

   from project_chameleon.rheedconverter import rheedconverter
   rheedconverter('new_image.img', 'new_image.png')

In this example, `'new_image.img'` is the raw RHEED image file containing the data. `'new_image.png'` is the name of the output file that will contain the converted image data. No metadata is collected or displayed by this function.

RHEED Video Converter
---------------------
``rheed_video_converter`` takes a RHEED `.imm` file as input, processes each video frame, and saves the adjusted video as a `.avi` or `.mp4` file. Here is an example of how the function ``rheed_video_converter`` can be used:

.. code-block:: python

   from project_chameleon.rheed_video_converter import rheed_video_converter
   rheed_video_converter('new_image.imm', 'new_video.avi', keep_images='0')

In this example, `'new_image.imm'` is the RHEED video file. `'new_video.avi'` is the output video file after conversion. The output format can be either `.avi` (lossless) or `.mp4` (lossy), depending on the desired compression.

The `keep_images` parameter is optional. If set to `'1'`, a folder will be created containing each video frame as a separate image file. If set to `'0'`, no frame images will be saved. This parameter defaults to `'0'`.


Below is more information on the main functions, as well as their helper functions:


.. automodule:: rheed_video_converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main

.. automodule:: rheedconverter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main

.. automodule:: rheed_helpers
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
