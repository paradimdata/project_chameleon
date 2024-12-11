==========================================
ARPES Data Workbook Creation
==========================================

This module contains a function called ``arpes_folder_workbook()``. ``arpes_folder_workbook()`` creates a workbook, looks through a specified folder to count how many scans there are, extracts values from `.pxt`, `.jaina`, and `.varian` files for each scan, and creates a row in the workbook for each scan. This function calls `build_arpes_workbook` and `insert_scan_row` to perform these tasks.

The function takes two arguments:
- ``folder_name``: A string or path to the folder containing the scan files.
- ``workbook_name``: A string or path for the name of the workbook to create. This should end with `.xlsx`.

Please note that if the `folder_name` is not a valid directory or if `workbook_name` does not end with `.xlsx`, exceptions will be raised.

.. automodule:: arpes
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: main