==========================================
Scanning Transmission Electron Microscopy
==========================================

This module contains functions for Scanning Transmission Electron Microscopy (STEM) data. There are two main functions in this module. ``non4dstem`` is designed to handle STEM files that are not 4D scans. It supports 2D and 3D `.dm4`, `.ser`, and `.emd` files. This function uses the Hyperspy package. Any files that can be processed by Hyperspy should also be compatible with this function. ``stemarray4d`` is designed to break down a 4D STEM `.raw` image into 2D images. This function uses the py4DSTEM package. Any files that can be processed by py4DSTEM should also work with this function.

4D STEM 
-------
``stemarray4d`` takes a 4D STEM `.raw` scan as input and converts it into a series of 2D `.png` image slices. There are three types of output: a folder containing the 2D image slices, a maximum projection image, and a mean projection image. Here is an example of how the function ``stemarray4d`` can be used:

.. code-block:: python

   from project_chameleon.stemarray4d import stemarray4d
   stemarray4d('example_file.raw', 'new_file')

In this example, `'example_file.raw'` is the STEM scan file containing the data. `'new_file'` is the base name used for all generated output files. The mean and max images will be labeled accordingly (e.g., `'new_file_max.png'`). The individual image slices will include the slice number (e.g., `'new_file13.png'`). No metadata is collected or displayed by this function.

Non-4D STEM
-----------
``non4dstem`` takes a non-4D `.dm4`, `.ser`, or `.emd` file as input and converts it into a plot saved as a `.png` file. This function supports both single file and folder inputs. Here is an example of how the function ``non4dstem`` can be used:

.. code-block:: python

   from project_chameleon.non4dstem import non4dstem
   non4dstem(data_file='test_file.ser', output_file='new_file.png')

In this example, `'test_file.ser'` is the non-4D STEM file containing the data, and `'new_file.png'` is the output image file for the resulting plot. To use the function with folders, replace ``data_file`` with ``data_folder``, and ``output_file`` with ``output_folder``. These parameters should be folder paths.

When processing folders, all compatible files in the specified input folder will be processed, and their plots will be saved as `.png` files in the output folder. No metadata is extracted or displayed by this function.


Below is more information on the main functions:


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
