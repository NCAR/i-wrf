=======================
I-WRF version |version|
=======================

.. image:: _static/I-WRF_banner_photo_web.png

Cornell University and the NSF National Center for Atmospheric Research have implemented a coordinated containerized framework for the `Weather Research and Forecasting Model (WRF) <https://www.mmm.ucar.edu/models/wrf>`_ that seamlessly integrates a new multi-node WRF container, the `enhanced Model Evaluation Tools (METplus) <https://dtcenter.org/community-code/metplus>`_ container, and an enhanced Analysis and Visualization container for more productive research. The `integrated WRF (I-WRF) <https://i-wrf.org/summary/index>`_ framework supports multi-node simulations, enabling research-grade applications, i.e., simulations covering large domains at high spatial discretization. The 4-year project began August 1, 2022 and its projected end date is July 31, 2026.

I-WRF’s coordinated capabilities and ease of use enable a wider range of researchers—from environmental engineering, transportation, civil engineering, air quality policy, hydrology, urban planning, agriculture, and more—to run their own modeling activities, followed by convenient interaction with the results, including evaluation and visualizations. The I-WRF container are designed for optimal portability and reproducibility of results for traceability of research.

The integrated framework and container features is tested and validated on the latest parallel HPC and cloud platforms by CI researchers and use case scientists who will scale studies on the evolution of renewable energy generation in a changing climate, the effect of land use and climate change on severe weather events, and the relation between air quality and human morbidity and mortality.

On the other end of the computational spectrum, these exact same containers serve as the vehicles for introducing students to numerical atmospheric simulations and output evaluation at WRF and METplus tutorials and in classroom curricula at universities.

To get started, begin by reviewing the `User's Guide documentation <https://i-wrf.readthedocs.io/en/latest/Users_Guide/index.html>`_.

User Support
------------

The `I-WRF GitHub Discussions Forum <https://github.com/NCAR/i-wrf/discussions>`_ is a place for questions, answers, and discussions concerning I-WRF. Users are encouraged to visit the Discussions Forum page to leave comments, ask I-WRF related questions, provide suggestions for future development, as well as report any bugs that are encountered when using the I-WRF framework.

Acronyms
--------

* **METplus** - Enhanced Model Evaluation Tools
* **NSF** - National Science Foundation
* **NCAR** - National Center for Atmospheric Research
* **RAL** - Research Applications Lab

.. toctree::
   :titlesonly:
   :maxdepth: 2 

   Users_Guide/index
   Users_Guide/overview
   Users_Guide/release-notes
   Users_Guide/compute-platform 
   Users_Guide/getting-started
   Users_Guide/configuration
   Users_Guide/use-cases/index
   Users_Guide/customization
   Users_Guide/references
