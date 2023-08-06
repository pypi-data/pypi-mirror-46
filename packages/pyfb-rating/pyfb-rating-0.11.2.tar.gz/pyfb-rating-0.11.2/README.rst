=============================
pyfb-rating
=============================

.. image:: https://badge.fury.io/py/pyfb-rating.svg
    :target: https://badge.fury.io/py/pyfb-rating

.. image:: https://travis-ci.org/mwolff44/pyfb-rating.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-rating

.. image:: https://codecov.io/gh/mwolff44/pyfb-rating/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-rating

Rating application for PyFB project

Documentation
-------------

The full documentation is at https://pyfb-rating.readthedocs.io.

Quickstart
----------

Install pyfb-rating::

    pip install pyfb-rating

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_rating.apps.PyfbRatingConfig',
        ...
    )

Add pyfb-rating's URL patterns:

.. code-block:: python

    from pyfb_rating import urls as pyfb_rating_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_rating_urls)),
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
