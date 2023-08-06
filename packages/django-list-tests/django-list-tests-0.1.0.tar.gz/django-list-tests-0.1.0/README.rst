=============================
django-list-tests
=============================


Add a django management command to list all tests in the project

Quickstart
----------

Install django-list-tests::

    pip install django-list-tests

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_list_tests',
        ...
    )


And run::

     ./manage.py list_tests <app_name>

