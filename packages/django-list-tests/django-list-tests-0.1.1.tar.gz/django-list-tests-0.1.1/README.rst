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


You can use this command for fzf completion of tests::

    # FZF ALL DAY ERRY DAY
    function tz() {
        # cache the test names to speed things up. you can go more complex with
        # watchman or whatever.
        if [[ ! -f '.test_names' ]]; then
            python $DJANGO_MANAGE_SCRIPT list_tests $DJANGO_ROOT_MODULE > ./.test_names
        fi

        TESTS=$( cat .test_names | fzf )

        echo Runnning "$TESTS"
        python "$DJANGO_MANAGE_SCRIPT" "test" --keepdb "$TESTS"
    }

