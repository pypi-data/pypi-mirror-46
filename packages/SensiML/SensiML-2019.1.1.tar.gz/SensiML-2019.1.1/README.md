=====================
SensiML Python CLient
=====================

SensiML python client provides access to SensiML Analytics services for
building machine learning pipelines including data processing, feature
generation and classification for developing smart sensor algorithms optimized
to run on embedded devices.

------------
Installation
------------

Download the Analytic Studio which will install a python 3 environment  along with all the requirements 
to run the SensiML Library.

    https://sensiml.cloud/downloads


You can also install directly from pypy repository using pip. We recommend  having python >= 3.7

    pip install sensiml -U

Our library is designed to be used within a jupyter notebook. For our
GUI to work correctly you will need to also install nbextension to
jupyter notebook. Installation instructions can be found here

https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html

You will need to enable the following extensions. bqplot, ipywidgets and qgrid.

    jupyter contrib nbextension install --user

    jupyter nbextension enable bqplot

    jupyter nbextension enable ipywidgets

    jupyter nbextension enable qgrid

----------------------------------
Connect to SensiML Analytic Engine
----------------------------------

Once you have installed the software, you can connect to the server by running the following
in a notebook cell.

    from sensiml import *

    sml = SensiML()

Connecting to SensiML servers requires and account, you can register at https://sensiml.cloud/accounts/register

Documentation can be found here https://sensiml.atlassian.net/wiki/spaces/SS/overview as well as in the Analytic Studio.

For information about SensiML, to get in touch, or learn more about using our platform to build
machine learning models suitable for performing real-time timeseries
classification on embedded devices you can reach us at https://sensiml.com/#contact


