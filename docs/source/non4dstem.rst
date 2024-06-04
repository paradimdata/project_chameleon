=================================================
Non-4D Scanning Transmission Electron Microscopy
=================================================

This module constains a function called 'non4dstem'. 'non4dstem' is designed to handle files associated with STEM that are not 4 dimension scans. This function has been designed around 2D and 3D .dm4, .ser, and .emd files. All files to be input should be put into a folder and the function will process each image in the folder. This function should be able to process any filetypes that can be processed by the hyperspy 'load' function. All outputs will be held in the folder named by the user input 'output_folder'.  

.. automodule:: non4dstem
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main