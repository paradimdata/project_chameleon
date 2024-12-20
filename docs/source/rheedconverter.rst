============================================
Reflection High-Energy Electron Diffraction
============================================

This module contains the functions for Reflection High-Energy Electron Diffraction (RHEED) data. These functions convert primarily two file types: RHEED .img images, and RHEED .imm video files. The ``rheedconverter`` function also functions for Crysalis Pro Single Crystal diffraction .img images. The two main functions in this module are ``rheedconverter`` and ``rheed_video_converter``. Other functions operate as helper functions for these two functions. Both functions perform the same function: convertering 16bpp images/videos to 8bpp images/videos. This can be a helpful step when working with RHEED data, as 16bpp images and videos are not easy to display on most typical systems. Some of the functions in this module operate based on specific headers in the file type for which this function was created. If you data does not have these headers, the functions may not work correctly. 

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