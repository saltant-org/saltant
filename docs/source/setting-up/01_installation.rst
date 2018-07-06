Installation
============

What follows is a rough draft for how to get set up with saltant.

Clone repo
----------

Clone the saltant repo. With HTTPS::

    $ git clone https://github.com/mwiens91/saltant.git

With SSH::

    $ git clone git@github.com:mwiens91/saltant.git

Set up virtual environment
--------------------------

First, enter the repositories directory::

    $ cd saltant

Using virtualenvwrapper, create a virtual environment named
``saltant-env``::

    $ mkvirtualenv -a . -p /usr/bin/python3 saltant-env

Now install requirements::

    $ pip install -r requirements.txt

Set up environment variables
----------------------------

saltant needs info unique to your locale, which it loads from a ``.env``
file. We'll fill in this file as we set up saltant. First we need to
create the ``.env`` from the template ``.env.example``::

    $ cp .env.example .env

One thing you should do now is generate a new secret key. One place to
generate a new key is here:

    https://www.miniwebtool.com/django-secret-key-generator/

Once that's done, make sure you replace the default key in ``.env`` with
they key you just generated.

Set up PostgreSQL
-----------------

Follow this guide for setting up PostgreSQL:

    https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

When it comes to modifying the DATABASES settings in ``settings.py``,
instead modify your ``.env`` file.

Once that's done, get the database migrated with ::

    $ ./manage migrate

Set up Redis server
-------------------

On Debian-like systems, install redis-server with ::

    $ sudo apt install redis-server

Now confirm that the server is running and responding::

    $ redis-cli ping
    PONG

If you didn't see PONG, something is terribly wrong.

Set up an admin user with an API authorization token
----------------------------------------------------

Create the admin user with ::

    $ ./manage createsuperuser

You will then be prompted for your username, email, and password::

    Username (leave blank to use 'matt'):
    Email address: matt@email.com
    Password:
    Password (again):
    Superuser created successfully.

Now we need to create an API authorization token for the admin user.
First enter the Django shell with ::

    $ ./manage shell

You should then see a prompt that looks like so::

    Python 3.6.5 (default, Apr  1 2018, 05:46:30)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]:

Great! This shell is enhanced with IPython, so you can use features like
tab completion to make your life easier.

To generate and print an API authorization token for the admin user,
enter the following at the Django shell::

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
the authorization key generated. Assign this key to the
``ADMIN_AUTH_TOKEN`` variable in your ``.env``.

Set up default TaskQueue and run Celery worker
----------------------------------------------

Wow. Very work!
