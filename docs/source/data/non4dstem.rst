==========================================
Scanning Transmission Electron Microscopy
==========================================

This module constains the functions for Scanning Transmission Electron Microscopy (STEM) data. There are two main functions in this module. ``non4dstem`` is designed to handle files associated with STEM that are not 4 dimension scans. This function has been designed around 2D and 3D .dm4, .ser, and .emd files. This function operates using the package hyperspy. Any files that can be processed by hyperspy should be able to be processed by this function. ``stemarray4d`` is designed to breakdown a 4D STEM .raw image into 2D images. This function uses the package py4DSTEM. Any files that can be processed by py4DSTEM should be able to be processed by this function.

4D STEM 
-------
``stemarray4d`` takes a 4D STEM .raw scan as an input and converts it into a series of 2D  .png image slices. There will be three outputs in total: a folder containing 2D slices of the image, a max image, and a mean image. Here is an example of how the function ``stemarray4d`` works:

.. code-block:: python

   from project_chameleon.stemarray4d import stemarray4d
   stemarray4d('example_file.raw','new_file')

In this example, the file 'example_file.raw' is the STEM scan file that holds the data. 'new_file' is the name that will be combine with a designator for all the generated output images. The mean and max images with be labeled accordingly and will look something like 'new_file_max.png'. The individual image slices with have the slice number attached and will look something like 'new_file13.png'. No metadata is collected or displayed as part of this function.

Non 4D STEM
-----------
``non4dstem`` take a non 4D .dm4, .ser, or .emd file as an input and converts it to a corresponding plot that is saved to a .png file. This function can handle both single file and folder inputs. Here is an example of how the function ``non4dstem`` can be used:

.. code-block:: python

   from project_chameleon.non4dstem import non4dstem
   non4dstem(data_file = 'test_file.ser', output_file = 'new_file.png')

In this example, the file 'test_file.ser' is the non 4D STEM file that hold the data. 'new_file.png' is the image file that the plot of the .ser file will be saved to. This is an example of how the function can be used for files. To use the function for folders, replace ``data_file`` with ``data_folder``, and replace ``output_file`` with ``output_folder``. These two new parameters should be folders. No metadata is collected or displayed as part of this function. When using this function for folders, all files that are processible in the given folder will be processed and their plots will be placed in .png files in the output folder. No metadata is extracted or displayed as part of this function.

Below is more information on the main functions.

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