Production server
=================

.. highlight:: console

As mentioned in the :doc:`introduction <introduction>`, the steps you
need to setup a saltant production server are very sensitive to your
particular environment and implementation needs. Hence, for this section
of installation instructions we will discuss *a* way to set up saltant
in production, not *the* way (and not necessarily even the "best" way).
This section continues directly from the :doc:`development` installation
instructions.

Allow incoming network traffic
------------------------------

For simplicity, assume we are using `AWS Route 53`_ to route traffic
from our domain, ``www.fictionaljobrunner.com``, to an `AWS EC2`_
instance used to host our saltant project, PostgreSQL database server,
and Redis server. These steps should translate over to most
implementation methods with (hopefully) minimal modification. We will
also assume that the PostgreSQL database server doesn't need to expose
itself to the network, and that the Redis server will need to expose
itself to the network.

Start by routing traffic from your domain to your EC2 instance by
following `these routing instructions`_.

Now, make sure you have ports open for SSH (22), HTTP (80), HTTPS (443),
and Redis (6379) traffic. [#aws-traffic]_ We will redirect HTTP requests
to HTTPS in `Let's encrypt!`_, and secure incoming Redis traffic with SSL
in `Secure Redis with SSL`_.

Set up production environment variables
---------------------------------------

We'll need to fill in production values for a few of our environment
variables, namely ``ALLOWED_HOSTS``, ``DJANGO_BASE_URL``, and ``DEBUG``
(which needs to be set to False!). Assuming that we've set up ALIAS DNS
records for ``fictionaljobrunner.com`` and
``www.fictionaljobrunner.com`` in the previous step, the relevant
variables of our ``.env`` file might look like

.. code-block:: shell

    # Insert hosts, separated by commas. Defaults to '127.0.0.1' if you
    # comment out this line. Wrap each host in single quotes, not double
    # quotes.
    ALLOWED_HOSTS='fictionaljobrunner.com','www.fictionaljobrunner.com','127.0.0.1'

    # Base URL of the site. Essentially just choose one of the allowed hosts
    # and prepend it with either "http://" or "https://". If hosting locally
    # add the port the site is being hosted on after the IP, as shown in the
    # below example.
    DJANGO_BASE_URL='https://www.fictionaljobrunner.com'

    # Defaults to 'False' if you comment out this line
    DEBUG=False

Hosting saltant on a socket with uWSGI
--------------------------------------

This and the next section are adapted from `these uWSGI and nginx
instructions`_, which provide a more detailed reference for the
following instructions.

First we need to install `uWSGI`_; if we're on Ubuntu we can install
it with ::

    $ sudo apt install uwsgi

We're going to daemonize saltant with the `uWSGI Emperor`_ and
`systemd`_. To do this we need to edit/create a few files:

**/etc/uwsgi/emperor.ini**

.. code-block:: ini

    [uwsgi]
    emperor = /etc/uwsgi/vassals
    uid = www-data
    gid = www-data
    logto = var/log/uwsgi-emperor.log

This file tells the uWSGI emperor to run the "vassals" in
``/etc/uwsgi/vassals``, one of which we will define now:

**/etc/uwsgi/vassals/saltant_uwsgi.ini**

.. code-block:: ini

    [uwsgi]
    chdir = /home/ubuntu/saltant
    module = saltant.wsgi
    home = /home/ubuntu/saltant/venv
    master = true
    processes = 10
    socket = /tmp/saltant.sock
    vacuum = true

This file defines a "vassal" which hosts saltant's WSGI module
``saltant.wsgi`` found at the root of the project
``/home/ubuntu/saltant`` using the project's virtual environment located
at ``/home/ubuntu/saltant/venv``. It also defines a socket to connect
to, ``/tmp/saltant.sock``. For more information, see `these uWSGI
Emperor
vassal instructions`_.

Next we need to daemonize the uWSGI Emperor we've just configured using
systemd:

**/etc/systemd/system/emperor.uwsgi.service**

.. code-block:: ini

    [Unit]
    Description=uWSGI Emperor for saltant
    After=syslog.target

    [Service]
    ExecStart=/usr/bin/uwsgi --ini /etc/uwsgi/emperor.ini
    RuntimeDirectory=uwsgi
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

Make sure this file is executable::

    $ sudo chmod +x /etc/systemd/system/emperor.uwsgi.service

Now you can enable the uWSGI-loaded saltant server with ::

    $ sudo servicectl enable emperor.uwsgi.service

Serving the socket with nginx
-----------------------------

We need to serve the socket with `nginx`_ so that the outside world can
interface with it.

First install and start nginx::

    $ sudo apt install nginx
    $ sudo /etc/init.d/nginx start

Now we need to edit the following file:

**/etc/nginx/sites-available/saltant_nginx.conf**

.. code-block:: nginx

    upstream django {
        server unix:///tmp/saltant.sock;
    }

    server {
        listen 80;
        listen [::]:80;

        server_name fictionaljobrunner.com www.fictionaljobrunner.com;

        charset utf-8;
        client_max_body_size 10M;

        location /static {
            alias /home/ubuntu/saltant/static;
        }

        location / {
            uwsgi_pass django;
            include /etc/nginx/uwsgi_params;
        }
    }

This will route HTTP traffic (which is not secure) to our saltant
project.

To enable this site, we need create the following sym link so nginx
knows to enable it::

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s ../sites-available/saltant_nginx.conf saltant_nginx.conf

Let's encrypt!
--------------

Thanks to `Let's Encrypt`_ and `EFF Certbot`_, securing our traffic with
SSL and redirecting all HTTP to HTTPS is ridiculously easy.

First install the Certbot for nginx with ::

    $ sudo apt install python-certbot-nginx

Then run it and follow its instructions with ::

    $ sudo certbot --nginx

Congrats to us! Now our site is secured with SSL with automatically
renewed certificates!

Secure Redis with SSL
---------------------

text here

Set up Flower with SSL
----------------------

text here

Set up Rollbar error tracking
-----------------------------

text here

Set up Papertrail log management
--------------------------------

text here

Footnotes
---------

.. Footnotes
.. [#aws-traffic] See https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html for instructions on opening EC2 instance ports.

.. Links
.. _AWS EC2: https://aws.amazon.com/ec2/
.. _AWS Route 53: https://aws.amazon.com/route53/
.. _EFF Certbot: https://certbot.eff.org/
.. _Let's Encrypt: https://letsencrypt.org/
.. _nginx: https://www.nginx.com/
.. _systemd: https://freedesktop.org/wiki/Software/systemd/
.. _these routing instructions: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html
.. _these uWSGI and nginx instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
.. _these uWSGI Emperor vassal instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#configuring-uwsgi-to-run-with-a-ini-file
.. _uWSGI: https://github.com/unbit/uwsgi
.. _uWSGI Emperor: https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html
