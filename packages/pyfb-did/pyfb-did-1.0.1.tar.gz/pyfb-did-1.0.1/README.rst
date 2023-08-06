=============================
pyfb-did
=============================

.. image:: https://badge.fury.io/py/pyfb-did.svg
    :target: https://badge.fury.io/py/pyfb-did

.. image:: https://travis-ci.org/mwolff44/pyfb-did.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-did

.. image:: https://codecov.io/gh/mwolff44/pyfb-did/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-did

Your project description goes here

Documentation
-------------

The full documentation is at https://pyfb-did.readthedocs.io.

Quickstart
----------

Install pyfb-did::

    pip install pyfb-did

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_did.apps.PyfbDidConfig',
        ...
    )

Add pyfb-did's URL patterns:

.. code-block:: python

    from pyfb_did import urls as pyfb_did_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_did_urls)),
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
