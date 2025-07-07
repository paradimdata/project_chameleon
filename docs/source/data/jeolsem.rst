==================================
JEOL Scanning Electron Microscopy
==================================

This module contains functions for Scanning Electron Microscopy (SEM) data. There are two main functions: ``sem_base_plot`` and ``sem_spectra_peak_labeler``. 

- ``sem_base_plot`` is designed to handle JEOL SEM `.EMSA` files and generate a clean base plot showing counts at each energy level with no labels.
- ``sem_spectra_peak_labeler`` also handles JEOL SEM `.EMSA` files, but instead of a clean base plot, it creates a plot with expected element peaks labeled. All other peaks are labeled with possible candidate elements.

``get_element_peaks`` is a helper function that extracts peak data for a given element from a pandas DataFrame. These functions are specifically written for JEOL files and may not work correctly with SEM data from other sources.

SEM Base Plot 
-------------
The ``sem_base_plot`` function takes a JEOL SEM `.EMSA` file as input, extracts the data, and creates a plot of counts versus energy level, which is saved as a `.png` file. Here's an example of how to use the function:

.. code-block:: python

   from project_chameleon.jeol_sem_converter import sem_base_plot
   sem_base_plot('jeol_sem.EMSA', 'jeol_sem.png', color='blue', label='test_plot')

In this example:
- `'jeol_sem.EMSA'` is the raw JEOL SEM file containing the energy count data.
- `'jeol_sem.png'` is the image file where the plot will be saved.
- `color='blue'` is an optional parameter that changes the plot color (defaults to black if not specified).
- `label='test_plot'` is an optional title for the plot (defaults to the file name if not provided).

This function does not extract any metadata; it only creates a plot of the data.

SEM Spectra Peak Labeler 
------------------------
The ``sem_spectra_peak_labeler`` function also takes a JEOL SEM `.EMSA` file as input, extracts the data, and creates a plot of counts versus energy level. It then labels expected peaks and identifies possible elements for unexpected peaks. The final labeled plot is saved as a `.png` file. Here's how to use the function:

.. code-block:: python

   from project_chameleon.jeol_sem_converter import sem_spectra_peak_labeler
   sem_spectra_peak_labeler('jeol_sem.EMSA', 'jeol_sem.png', elements_in_plot='H,He,Li')

In this example:
- `'jeol_sem.EMSA'` is the input SEM file.
- `'jeol_sem.png'` is the output plot file.
- `elements_in_plot='H,He,Li'` is an optional comma-separated string of expected elements. All listed elements will be labeled in the plot, whether or not a peak is present at those energies. Peaks not matching any of the specified elements will be labeled with possible element candidates.

This function does not extract any metadata; it only creates a labeled plot of the data.


Below is more information on the main functions, as well as some helper functions:


.. automodule:: jeol_sem_converter
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main
