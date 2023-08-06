=============================
pyfb-endpoint
=============================

.. image:: https://badge.fury.io/py/pyfb-endpoint.svg
    :target: https://badge.fury.io/py/pyfb-endpoint

.. image:: https://travis-ci.org/mwolff44/pyfb-endpoint.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-endpoint

.. image:: https://codecov.io/gh/mwolff44/pyfb-endpoint/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-endpoint

Endpoint app for PyFreeBilling

Documentation
-------------

The full documentation is at https://pyfb-endpoint.readthedocs.io.

Quickstart
----------

Install pyfb-endpoint::

    pip install pyfb-endpoint

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_endpoint.apps.PyfbEndpointConfig',
        ...
    )

Add pyfb-endpoint's URL patterns:

.. code-block:: python

    from pyfb_endpoint import urls as pyfb_endpoint_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_endpoint_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
