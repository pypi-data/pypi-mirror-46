=============================
django-ratings-models
=============================

.. image:: https://badge.fury.io/py/django-ratings-models.svg
    :target: https://badge.fury.io/py/django-ratings-models

.. image:: https://requires.io/github/exolever/django-ratings-models/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-ratings-models/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-ratings-models.svg?branch=master
    :target: https://travis-ci.org/exolever/django-ratings-models

.. image:: https://codecov.io/gh/exolever/django-ratings-models/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-ratings-models

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-ratings-models&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-ratings-models
   
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-ratings-models/issues
   
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT


Ratings for your Django models


Quickstart
----------

Install django-ratings-models::

    pip install django-ratings-models

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ratings',
        ...
    )

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
