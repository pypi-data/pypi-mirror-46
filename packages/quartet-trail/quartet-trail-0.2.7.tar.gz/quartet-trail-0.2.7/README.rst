=============================
Quartet Trail
=============================

.. image:: https://gitlab.com/lduros/quartet-trail/badges/master/coverage.svg
   :target: https://gitlab.com/lduros/quartet-trail/pipelines
.. image:: https://gitlab.com/lduros/quartet-trail/badges/master/build.svg
   :target: https://gitlab.com/lduros/quartet-trail/commits/master
.. image:: https://badge.fury.io/py/quartet-trail.svg
    :target: https://badge.fury.io/py/quartet-trail

Logs action in Quartet

Documentation
-------------

The full documentation is at https://lduros.gitlab.io/quartet-trail/

Quickstart
----------

Install Quartet Trail::

    pip install quartet-trail

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'quartet_trail.apps.QuartetTrailConfig',
        ...
    )

Add Quartet Trail's URL patterns:

.. code-block:: python

    from quartet_trail import urls as quartet_trail_urls


    urlpatterns = [
        ...
        url(r'^', include(quartet_trail_urls)),
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

