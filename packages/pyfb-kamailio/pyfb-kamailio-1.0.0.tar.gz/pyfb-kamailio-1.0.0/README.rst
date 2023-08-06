=============================
Pyfb-kamailio
=============================

.. image:: https://badge.fury.io/py/pyfb-kamailio.svg
    :target: https://badge.fury.io/py/pyfb-kamailio

.. image:: https://travis-ci.org/mwolff44/pyfb-kamailio.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-kamailio

.. image:: https://codecov.io/gh/mwolff44/pyfb-kamailio/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-kamailio

Kamailio package for django project, mainly used by PyFreeBilling project

Documentation
-------------

The full documentation is at https://pyfb-kamailio.readthedocs.io.

Quickstart
----------

Install Pyfb-kamailio::

    pip install pyfb-kamailio

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_kamailio.apps.PyfbKamailioConfig',
        ...
    )

Add Pyfb-kamailio's URL patterns:

.. code-block:: python

    from pyfb_kamailio import urls as pyfb_kamailio_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_kamailio_urls)),
        ...
    ]

Apply migrations :

    python manage.py migrate

Upload initial data :

    python manage.py loaddata pyfb_kamailio

Features
--------

Kamailio modules supported by this application :

* acc
* dialog
* htable
* mtree
* permissions
* pipelimit
* registrar
* rtpengine
* speeddial
* uac
* userblacklist
* userloc

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
