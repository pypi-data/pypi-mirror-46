Datapunt user admin
===================

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
    :target: https://www.mozilla.org/en-US/MPL/2.0/

---------------------

Install
-------

::

    $ pip install datapunt-user

In order to use this library you need to have access to a Postgress database.

Usage
-----

::

    import dpuser

    users = dpuser.AuthzMap(**psycopgconf)

    users.add('myuser@example.com', 'secretpassword')
    users.set('myuser@example.com', 'newsecretpassword')
    users.verify_password('myuser@example.com', 'secretpassword')
    users.remove('myuser@example.com')


Contribute
----------

Activate your virtualenv, install the egg in `editable` mode, and start coding:

::

    $ source env/bin/activate
    $ pip install -e .

Testing:

::

    make test
