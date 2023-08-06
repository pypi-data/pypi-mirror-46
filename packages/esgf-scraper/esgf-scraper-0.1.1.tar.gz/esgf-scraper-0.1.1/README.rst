ESGF Scraper
============

.. sec-begin-index

+-------------------+----------------+-----------+
| Repository health | |Build Status| | |Codecov| |
+-------------------+----------------+-----------+

ESGF Scraper is a tool for downloading and processing climate data from the Earth System Grid Federation (ESGF_). ESGF is an international
collaborative network specifically designed for dissemination of climate model output for large scale projects such as CMIP6.

.. _ESGF: https://esgf.llnl.gov/

.. |Build Status| image:: https://gitlab.com/magicc/esgf-scraper/badges/master/pipeline.svg
    :target: https://gitlab.com/magicc/esgf-scraper/commits/master
.. |Codecov| image:: https://gitlab.com/magicc/esgf-scraper/badges/master/coverage.svg?job=test
    :target: https://gitlab.com/magicc/esgf-scraper/commits/master

.. sec-end-index

Documentation
-------------
See the `documentation <https://magicc.gitlab.io/esgf-scraper/>`_ for examples of using ``esgf-scraper``

.. sec-begin-installation

Installation
------------

esgf-scraper is not currently `pip <https://pypi.org/project/pip/>`_ installable as the code is not publically accessible. To install, you must checkout the
code from `GitLab <https://gitlab.com/magicc/esgf-scraper>`_.

::

  git clone git@gitlab.com:magicc/esgf-scraper.git
  cd esgf-scraper
  make virtual-environment
  cp esgf_scraper.conf.sample ~/esgf_scraper.conf

After this has been completed, the configuration file will need to be updated with new configuration. See TODO for more information
about the contents of the configuration file.

.. sec-end-installation

Contributing
------------

If you'd like to contribute, please make a pull request!
The pull request templates should ensure that you provide all the necessary information.

.. sec-begin-license

License
-------

This package is licensed under a `MIT license <https://opensource.org/licenses/MIT>`_, unless noted otherwise for specific parts.

.. sec-end-license