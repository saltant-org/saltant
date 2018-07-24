Development server setup
========================

.. highlight:: console

What follows are instructions for how to set up a local development
server for saltant. The next section, :doc:`production`, directly
follows this and describes how to serve saltant in production.

Cloning the saltant repository
------------------------------

The first thing you need to do is clone the saltant repository. With
HTTPS, do this with ::

    $ git clone https://github.com/mwiens91/saltant.git

Or with SSH, do it with ::

    $ git clone git@github.com:mwiens91/saltant.git

Setting up a virtual environment
--------------------------------

Next you need to set up saltant's environment. First, enter the
repository's directory::

    $ cd saltant

Create and activate a new Python 3.x virtual environment using your
preferred method, or with ::

    $ python3 -m venv venv
    $ source venv/bin/activate

After you've activated a virtual environment, you need to install
saltant's requirements::

    $ pip install -r requirements.txt

Setting up environment variables
--------------------------------

saltant needs to collect variables unique to your locale. When its
server is run, saltant loads these variables from an ``.env`` text file
at the base of the repository.

To create your ``.env`` file, copy the included example ``.env.example``
file to ``.env``::

    $ cp .env.example .env

Go ahead and fill in the ``PROJECT_NAME`` variable with the name of your
project.  Also make *sure* you generate and fill in a new ``SECRET_KEY``
for your project (keep it secret). [#secretkey]_ One option for
generating a unique secret key is to use `this site
<https://www.miniwebtool.com/django-secret-key-generator/>`_.

We will fill in the rest of the ``.env`` as we continue through the
hosting instructions.

Setting up a PostgreSQL database
--------------------------------

The next step is to set up a PostgreSQL database for the project; for
simplicity it assumes you are using a Debian-like operating system
(e.g., Ubuntu). [#postgres_reference]_ First, make sure you have the
necessary packages; on Ubuntu, these packages can be installed with ::

    $ sudo apt install python3-dev libpq-dev postgresql postgresql-contrib

The next step is to launch a Postgres session as the ``postgres`` user::

    $ sudo -u postgres psql

You should see a prompt like the following::

    psql (10.4 (Ubuntu 10.4-0ubuntu0.18.04), server 9.6.8)
    Type "help" for help.

    postgres=#

Now, having the project name ``project``, a username ``username``, and
password ``password`` in mind, enter the following commands:
[#postgres_commands]_

.. code-block:: none

    postgres=# CREATE DATABASE project;
    postgres=# CREATE USER username WITH PASSWORD 'password';
    postgres=# ALTER ROLE username SET client_encoding TO 'utf8';
    postgres=# ALTER ROLE username SET default_transaction_isolation TO 'read committed';
    postgres=# ALTER ROLE username SET timezone TO 'UTC';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE project TO username;
    postgres=# \q

Once that's done fill in the corresponding variables (``DATABASE_NAME``,
``DATABASE_USER``, and ``DATABASE_USER_PASSWORD``) in your ``.env``.

Migrate in saltant's database schema with ::

    $ ./manage migrate

Setting up an admin account
---------------------------

Create an admin user by running the following::

    $ ./manage createsuperuser

You should be prompted for your username, email, and password::

    Username (leave blank to use 'matt'):
    Email address: matt@email.com
    Password:
    Password (again):
    Superuser created successfully.

Note that the Django admin user credentials are completely independent
of the credentials for the PostgreSQL user associated with your
project's database.

Generating an admin API authentication token
--------------------------------------------

Now you need to create an API authentication token for the admin user
you just created. First enter the Django shell with ::

    $ ./manage shell

You should then see a prompt that looks like so:

.. code-block:: python3

    Python 3.6.5 (default, Apr  1 2018, 05:46:30)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]:

Great! This shell is enhanced with IPython, so we can use features like
tab completion to make our life easier.

To generate and print an API authentication token for the admin user,
enter the following in the Django shell you just opened:

.. code-block:: python3

    Python 3.6.5 (default, Apr  1 2018, 05:46:30)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from django.contrib.auth.models import User

    In [2]: admin_user = User.objects.get(id=1)

    In [3]: from rest_framework.authtoken.models import Token

    In [4]: token = Token.objects.create(user=admin_user)

    In [5]: print(token.key)
    9840c08189e030873387a73b90ada981885010dd

In this example, ``9840c08189e030873387a73b90ada981885010dd`` would be
the API authentication token that was generated. Set the
``API_AUTH_TOKEN`` variable in your ``.env`` to the value of this token.

Setting up a local RabbitMQ server
----------------------------------

On Debian-like systems, setting up a local RabbitMQ server is dead
simple::

    $ sudo apt install rabbitmq-server

The RabbitMQ server is used as a message broker to talk to workers that
consume the tasks that are created with saltant.

Setting up a TaskQueue with a Celery worker
-------------------------------------------

Define where local Celery workers should store log files and Singularity
images by setting the ``WORKER_LOGS_DIRECTORY`` and
``WORKER_SINGULARITY_IMAGES_DIRECTORY`` variables in your ``.env``.

Now we need to launch a Celery worker to consume tasks, but before we do
that we need to register a TaskQueue for our worker. To create the
TaskQueue, launch the Django shell again and enter the following
commands:

.. code-block:: python3

    Python 3.6.5 (default, Apr  1 2018, 05:46:30)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from tasksapi.models import TaskQueue

    In [2]: TaskQueue.objects.create(name="default",
       ...:                          description="the default queue")
       ...:
    Out[2]: <TaskQueue: default>

Now, to run a Celery worker to consume from the queue named
``default``, run ::

    $ celery worker -A saltant -Q default

Running the server
------------------

Now all you should need to do is ::

    $ ./manage runserver

and point your browser to ``127.0.0.1``!

.. Footnotes
.. [#secretkey] The secret key is used for cyptographic signing.  See
    `here
    <https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key>`_
    for details.
.. [#postgres_reference] The instructions for setting up PostgreSQL are
    adapted from `here
    <https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04>`_.
.. [#postgres_commands] See `here
    <https://docs.djangoproject.com/en/2.1/ref/databases/#optimizing-postgresql-s-configuration>`_
    for more context on these commands.
