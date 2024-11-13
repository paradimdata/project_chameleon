---
title: 'Project Chameleon: A Python package for material science research'
tags:
  - Python
  - material science
  - crystal growth
  - reflection high-energy electron diffraction
  - angle-resolved photoemission spectroscopy
  - molecular beam epitaxy
  - scanning transmission electron microscopy
  - x-ray diffraction
authors:
  - name: Peter Julien Kohler Cauchy
    orcid: 0009-0007-1155-0509
    equal-contrib: true
    affiliation: "1, 2, 3"
  - name: David Elbert
    orcid: 0000-0002-2292-180X
    corresponding: true
    affiliation: "1, 2"
affiliations:
 - name: National Science Foundation (Platform for the Accelerated Realization, Analysis, and Discovery of Interface Materials (PARADIM))
   index: 1
 - name: Johns Hopkins University, Baltimore, Maryland, USA
   index: 2
 - name: Cornell University, Ithaca, New York, USA
   index: 3
date: 13 November 2024
---

# Summary

When developing new material configurations and crystal structures, it is important to thoroughly test them to ensure they have the desired and expected properties. In the matierial science field, there are many different tools and measurements used to characterize materials, including, but not limited to, diffraction, microscopy, and spectroscopy. While these methods are commonly used, they often dictate the use of specific tools, which in turn requires specific workflows and software be followed to interpret results.  

# Statement of Need

`Project Chameleon` is a python package for processing files commonly found in material science research. Python allows for the reading and processing of a wide variety of file types that typically need specific software to process. The API for `Project Chameleon` was designed to provide a function-based user-friendly interface that allows simple conversions of some common file types. The API has also been designed to handle multiple input and ouput types, including raw bytes, json, and URLs, giving flexibility in how it can be implemented. `Project Chameleon` also relies on packages that have done elements of the conversion and processing. These packages include xylib, hyperspy, py4dstem, and htmdec_formats. 

`Project Chameleon` was designed to be used by material science researchers, but could potentially have uses in other fields of research. `Project Chameleon` is already in use in one material science lab, McQueen Lab at Johns Hopkins University, where the brukerraw function is used to convert raw XRD files to csv files, and the hs2 function is use to convert Laue .hs2 images to .png images. Both of these functions have been integrated into the lab file server, allowing for the download of the raw file or converted file without any work done on the users end. Further integrations such as this one will allow for signifcant leaps in the efficiency and flexibility of material science workflows that include these file types.  

# Mathematics

Not sure if I need this section. I added it since it's in the example but Chameleon doesn't have as much math specific stuff as the example did. 

# Citations

I am not sure if I have anything I need to cite. Do I need to cite xylib, py4stem, hyperspy, and htmdecs since I mentioned them? Is there anything else?

# Figures

Do I need any figures? Should  I include any processed images or anything like that?

# Acknowledgements 

We acknowledge contributions and support from Maggie Eminizer and Matt Turk. Their help was key to helping this project get done.

# References

Do I need any references?