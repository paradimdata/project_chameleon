==========================================
Scanning Transmission Electron Microscopy
==========================================

This module constains the functions for Scanning Transmission Electron Microscopy (STEM) data. There are two main functions in this module. ``non4dstem`` is designed to handle files associated with STEM that are not 4 dimension scans. This function has been designed around 2D and 3D .dm4, .ser, and .emd files. This function operates using the package hyperspy. Any files that can be processed by hyperspy should be able to be processed by this function. ``stemarray4d`` is designed to breakdown a 4D STEM .raw image into 2D images. This function uses the package py4DSTEM. Any files that can be processed by py4DSTEM should be able to be processed by this function.

.. automodule:: non4dstem
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main

.. automodule:: stemarray4d
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main