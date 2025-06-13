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

Project Chameleon is a versatile Python package for extensible data transformation and interoperability. Chameleon streamlines analysis and combination of scientific data from different sources and provides a foundational pillar for implementation of the FAIR (Findable, Accessible, Interoperable, and Reusable) data principles[1]. In the context of FAIR, interoperability refers to the ability of diverse datasets, tools, and systems to seamlessly interact, integrate, and exchange data. Interoperability ensures that scientific data can be readily combined or used alongside related datasets, software, and analytical tools across different domains and disciplines.  A central barrier to interoperability arises from heterogeneous data formats and differing metadata conventions encoded in the varied file formats of different laboratories.  Project Chameleon transformations eliminate this barrier to provide effective interoperability that facilitates comprehensive analyses and machine learning that accelerate scientific discovery and enhance reproducibility of scientific findings.
Project Chameleon provides a collection of conversion scripts accessed through a REST API that enables researchers to simply convert specialized, often manufacturer-specific file formats for data such as RHEED electron diffraction patterns, scanning transmission electron microscopy (STEM) arrays, molecular beam epitaxy (MBE) logs, magnetic property measurement system analyses (PPMS/MPMS), and X-ray diffraction patterns into universally accessible formats like CSV for tabular data and PNG for image data. These universal formats provide the research community the ability to use open and readily available tools to analyze and visualize data from different instruments or laboratories. The API for Project Chameleon provides a function-based, user-friendly interface that allows simple conversions of some common file types. The API is also designed to handle multiple input and output types, including raw bytes, json, and URLs, giving flexibility in how it can be implemented. Project Chameleon itself leverages several open source packages for conversion and processing of specialized formats [2-5].  

# Statement of Need

The U.S. interagency Materials Genome Initiative[6-10] demands a leap in FAIR-compliant data to accelerate materials discovery, AI/ML applications, high-throughput experimentation, advanced digital twins, and growing interest in autonomous laboratories and manufacturing. Fundamental research in materials science, chemistry, and solid-state physics, however, depends on structure and property characterizations that use a wide range of techniques including, but not limited to, diffraction, microscopy, and spectroscopy. While these methods are a common thread in modern science, they rely on a wide variety of laboratory instrumentation developed by a wide range of manufacturers, creating a multitude of data formats demanding use of specialized analysis tools; The wide variation in data formats hinders FAIR interoperability; the inability to combine data from different sources or reproduce analyzes done in different labs thwarts Open Science and MGI goals. 

`Project Chameleon` was designed to be used by material science researchers, but is applicable to any field of research using instrumental characterization tools. `Project Chameleon` is already in use in the NSF PARADIM Materials Innovation Platform (Cornell and Johns Hopkins universities) as well as the McQueen Lab at Johns Hopkins where the ARPES, Bruker RAW, Bruker BRML, 4D STEM, Non-4D STEM, RHEED, MBE, PPMS/MPMS, Laue HS2, and JEOL SEM functions have been implemented. These functions are used in the lab file server for McQueen Lab and to create FAIR datasets published with DOIs in the PARADIM Data Portal[11], allowing for the download of the raw file or converted file without any work done on the users end. Further integrations such as this one will allow for significant leaps in the efficiency and flexibility of material science workflows that include these file types. 
  


# Citations

@article{wilkinson2016fair,
  author  = {Wilkinson, Mark D. and Dumontier, Michel and Aalbersberg, IJsbrand Jan and Appleton, Gavin and Axton, Myles and Baak, Arie and Blomberg, Niklas and Boiten, Jan Willem and da Silva Santos, Luiz Bonino and Bourne, Philip E. and others},
  title   = {The FAIR Guiding Principles for scientific data management and stewardship},
  journal = {Scientific Data},
  volume  = {3},
  year    = {2016},
  issn    = {2052-4463},
  doi     = {10.1038/sdata.2016.18}
}

@article{savitzky2021py4dstem,
  author  = {Savitzky, Benjamin H. and others},
  title   = {py4DSTEM: a software package for four-dimensional scanning transmission electron microscopy data analysis},
  journal = {Microscopy and Microanalysis},
  volume  = {27},
  pages   = {712},
  year    = {2021},
  doi     = {10.1017/S1431927621003251}
}

@software{pena2025hyperspy,
  author    = {Peña, Francisco de la and others},
  title     = {{Hyperspy/Hyperspy: V2.3.0}},
  version   = {v2.3.0},
  date      = {2025-03-02},
  publisher = {Zenodo},
  url       = {https://doi.org/10.5281/zenodo.14956374},
  doi       = {10.5281/zenodo.14956374}
}

@software{wojdyr2025xylib,
  author    = {Wojdyr, Marcin},
  title     = {{Wojdyr/Xylib}},
  year      = {2025},
  date      = {2025-05-24},
  url       = {https://github.com/wojdyr/xylib},
  note      = {GitHub repository}
}

@software{htmdec2025formats,
  author    = {{HTMDEC}},
  title     = {{Htmdec/Htmdec\_formats}},
  year      = {2025},
  date      = {2025-01-17},
  url       = {https://github.com/htmdec/htmdec_formats},
  note      = {High-Throughput Materials Discovery for Extreme Conditions (HTMDEC), GitHub repository}
}

@misc{ostp2021mgi,
  author       = {{U.S. White House Office of Science and Technology Policy}},
  title        = {Materials Genome Initiative Strategic Plan},
  year         = {2021},
  url          = {https://www.mgi.gov/sites/default/files/documents/MGI-2021-Strategic-Plan.pdf},
  note         = {Accessed 2025-06-13}
}

@article{brinson2024fair,
  author  = {Brinson, L. C. and Bartolo, L. M. and Blaiszik, B. and others},
  title   = {Community action on FAIR data will fuel a revolution in materials research},
  journal = {MRS Bulletin},
  volume  = {49},
  pages   = {12--16},
  year    = {2024},
  doi     = {10.1557/s43577-023-00498-4}
}

@article{odegard2023strategy,
  author  = {Odegard, G. M. and Liang, Z. and Siochi, E. J. and others},
  title   = {A successful strategy for MGI-inspired research},
  journal = {MRS Bulletin},
  volume  = {48},
  pages   = {434--438},
  year    = {2023},
  doi     = {10.1557/s43577-023-00525-4}
}

@article{depablo2019frontiers,
  author  = {de Pablo, Juan J. and Jackson, Nicholas E. and Webb, Michael A. and others},
  title   = {New frontiers for the materials genome initiative},
  journal = {npj Computational Materials},
  volume  = {5},
  pages   = {41},
  year    = {2019},
  doi     = {10.1038/s41524-019-0173-4}
}

@book{nasem2024digitaltwins,
  author    = {{National Academies of Sciences, Engineering, and Medicine}},
  title     = {Foundational Research Gaps and Future Directions for Digital Twins},
  year      = {2024},
  publisher = {The National Academies Press},
  address   = {Washington, DC},
  doi       = {10.17226/26894},
  url       = {https://doi.org/10.17226/26894}
}

@online{paradimdata,
  title        = {PARADIM Data Portal},
  year         = {2025},
  url          = {https://data.paradim.org/index.php},
  note         = {Accessed: 2025-06-13},
  organization = {Platform for the Accelerated Realization, Analysis, and Discovery of Interface Materials (PARADIM)}
}


# Acknowledgements 

We acknowledge contributions and support from Maggie Eminizer, Matt Turk, Ali Rachidi, Steve Zeltman, Ben Redemann, Abby Neil, and Evan Crites.  
