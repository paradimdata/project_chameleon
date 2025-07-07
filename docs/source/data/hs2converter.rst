===========================
Laue .hs2 X-Ray Diffraction
===========================

This module contains a function for processing Laue `.hs2` X-Ray Diffraction data. The function is designed to convert Laue `.hs2` image files into `.png` images. These images are converted from 16 bits per pixel (16bpp) to 8 bits per pixel (8bpp). Since 16bpp images are often difficult to open on standard systems, this function allows them to be more easily read and processed.

HS2 Converter 
-------------
The ``hs2converter`` function takes a Laue `.hs2` file as input, converts the image data from 16bpp to 8bpp, and writes it to a `.png` file. Here is an example of how the function can be used:

.. code-block:: python

   from project_chameleon.hs2converter import hs2converter
   hs2converter('example.hs2', 'example.png')

In this example, the file `'example.hs2'` is the Laue file containing the scan data. `'example.png'` is the output file where the image will be saved. This function supports images with two different resolutions: 256 × 256 and 512 × 512.


Below is more information on the main function, as well as some of the helper functions:


.. automodule:: hs2converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
