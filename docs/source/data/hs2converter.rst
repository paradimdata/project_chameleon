===========================
Laue .hs2 X-Ray Diffraction
===========================

This module contains the function for Laue hs2 X-Ray Diffraction data. This function was designed to convert Laue .hs2 X-Ray Diffraction images to .png images. The Laue images are converted from 16bpp images to 8bpp images. 16bpp images are typically hard to open on typical systems, so this function allows the images to be more easily read and processed.

HS2 Converter 
-------------
``hs2converter`` takes a Laue .hs2 files as an input, converts the image data from 16bpp to 8bpp, and writes it into a .png file. Here is an example of how the function ``hs2converter`` can be used:

.. code-block:: python

   from project_chameleon.hs2converter import hs2converter
   hs2converter('example.hs2','example.png')

In this example. the file 'example.hs2' is the Laue .hs2 file that holds the scan data. 'example.png' is the .png file that the data will be written to. This function can handle images with two different sets of dimensions: 256 x 256 and 512 x 512. 

Below is more information on the main functions, as well as some of the helper functions.

.. automodule:: hs2converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main