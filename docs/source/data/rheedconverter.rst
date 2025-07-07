============================================
Reflection High-Energy Electron Diffraction
============================================

This module contains the functions for Reflection High-Energy Electron Diffraction (RHEED) data. These functions convert primarily two file types: RHEED .img images, and RHEED .imm video files. The ``rheedconverter`` function also functions for Crysalis Pro Single Crystal diffraction .img images. The two main functions in this module are ``rheedconverter`` and ``rheed_video_converter``. Other functions operate as helper functions for these two functions. Both functions perform the same function: convertering 16bpp images/videos to 8bpp images/videos. This can be a helpful step when working with RHEED data, as 16bpp images and videos are not easy to display on most typical systems. Some of the functions in this module operate based on specific headers in the file type for which this function was created. If you data does not have these headers, the functions may not work correctly. 

RHEED Image Converter 
---------------------
``rheedconverter`` takes a RHEED .img file as an input, extracts all image data, and converts it to a .png file. Here is an example of how the function ``rheedconverter`` can be used:

.. code-block:: python

   from project_chameleon.rheedconverter import rheedconverter
   rheedconverter('new_image.img','new_image.png')

In this example, the file 'new_image.img' is the raw RHEED image that holds the data. 'new_image.png' is the name of the image file that will hold the adjusted data. No metadata is collected or displayed as part of this function. 

RHEED Video Converter
---------------------
``rheed_video_converter`` takes a RHEED .imm file as an input, operates on each video frame, and saves adjusted video as a .avi or .mp4 file. Here is an example of how the function ``rheed_video_converter`` can be used:

.. code-block:: python

   from project_chameleon.rheed_video_converter import rheed_video_converter
   rheed_video_converter('new_image.imm','new_video.avi', keep_images = '0')

In this example. the file 'new_image.imm' in the RHEED video files. 'new_video.avi' is the adjust video file that will be produced after the video is adjusted. The output names can have two possible extensions: .avi and .mp4. These extensions directly affect the video generated with .avi being lossless and .mp4 being lossy. The parameter 'keep_images' is an optional parameter. If set to '1', a folder will be created along with the adjusted video that holds each frame of the video as it's own image file. If set to '0', no images will be created. This parameter defaults to '0'. 

Below is more information on the main functions, as well as some of the helper functions.

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