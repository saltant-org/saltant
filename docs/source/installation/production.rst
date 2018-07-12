Production server setup
=======================

.. highlight:: console

As mentioned in the :doc:`introduction <introduction>`, the steps you
need to setup a saltant production server are very sensitive to your
particular environment and implementation needs. Hence, for this section
of installation instructions we will discuss *a* way to set up saltant
in production, not *the* way (and not necessarily even the "best" way).
This section continues directly from the :doc:`development`
instructions.

Allowing incoming network traffic
---------------------------------

For simplicity, assume we are using `AWS Route 53`_ to route traffic
from our domain, ``www.fictionaljobrunner.com``, to an `AWS EC2`_
instance used to host our saltant project, PostgreSQL database server,
and Redis server. These steps should translate over to most
implementation methods with (hopefully) minimal modification. We will
also assume that the PostgreSQL database server doesn't need to expose
itself to the network, and that the Redis server will need to expose
itself to the network.

Start by routing traffic from your domain to your EC2 instance by
following. Set up ALIAS DNS records for ``fictionaljobrunner.com`` and
``www.fictionaljobrunner.com``. You may find `these routing
instructions`_ helpful.

Now, make sure you have ports open for SSH (22), HTTP (80), HTTPS (443),
and Redis (6379) traffic. [#aws-traffic]_ We will redirect HTTP requests
to HTTPS in `Let's encrypt!`_, and secure incoming Redis traffic with SSL
in `Secure Redis with SSL`_.

Setting up production environment variables
-------------------------------------------

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
    logto = /var/log/uwsgi-emperor.log

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
to, ``/tmp/saltant.sock``, and declares that it can handle ``10``
requests from that socket simultaneously. For more information, see
`these uWSGI Emperor vassal instructions`_.

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

Hosting Redis on a network
--------------------------

Now let's focus on Redis. If all of your Celery workers will be running
on the local machine, then you can safely ignore this section.

We're going to need to change a few things in the Redis config file,
which is located at ``/etc/redis/redis.conf``. First we'll add our
machine's IP (let's suppose it's 192.168.1.100) to the list of IPs that
Redis should bind to. Look for the line ::

    bind 127.0.0.1 ::1

and add your machines IP to it like so::

    bind 192.168.1.100 127.0.0.1 ::1

Next we're going to need to tell Redis that it's okay to accept clients
from other hosts. Look for the line ::

    protected-mode yes

and change it to ::

    protected-mode no

Optionally, we can set a password that clients must provide when
connecting. Say we want to set the password to ``Hunter2``. Look for the
line

.. code-block:: shell

    # requirepass foobared

and change it to ::

    requirepass Hunter2

Now that we've done this, we need to update the ``CELERY_BROKER_URL``
and ``CELERY_RESULT_BACKEND`` variables in our project's ``.env`` file,
keeping in mind our machine's IP 192.168.1.100 and the ``Hunter2``
password we just required clients provide:

.. code-block:: shell

    CELERY_BROKER_URL='redis://:Hunter2@192.168.1.100:6379'
    CELERY_RESULT_BACKEND='redis://:Hunter2@192.168.1.100:6379'

Secure Redis with SSL
---------------------

Securing Redis is only necessary if you plan on exposing it to a
potentially unsafe network (e.g., the internet). If all of your Celery
workers will be connected to Redis on a secure network, feel free to
ignore this section.

We will be securing Redis using `stunnel`_. [#stunnel-reference]_
[#stunnel-better-way]_ First install stunnel::

    $ sudo apt install stunnel4

Enable it by editing the stunnel's config file at
``/etc/default/stunnel4`` and changing

.. code-block:: shell

    ENABLED=0

to

.. code-block:: shell

    ENABLED=1

Now we need to create a key to use for generating a certificate::

    $ sudo openssl genrsa -out /etc/stunnel/key.pem 409

To create the actual certificate that will expire in 9999 days (edit
this number as you please), run ::

    $ sudo openssl req -new -x509 -key /etc/stunnel/key.pem -out /etc/stunnel/cert.pem -days 9999

and answer the questions that it asks you.

Now let's combine the key and the certificate so that stunnel can use
it::

    $ sudo cat /etc/stunnel/key.pem /etc/stunnel/cert.pem > ~/private.pem
    $ sudo mv ~/private.pem /etc/stunnel/private.pem
    $ sudo chmod 640 /etc/stunnel/key.pem /etc/stunnel/cert.pem /etc/stunnel/private.pem

Assuming again that our machine's IP is 192.168.1.100, create a file
``/etc/stunnel/redis-server.conf`` with contents

.. code-block:: ini

    cert = /etc/stunnel/private.pem
    pid = /var/run/stunnel.pid
    [redis]
    accept = 192.168.1.100:6379
    connect = 127.0.0.1:6379

Start stunnel with ::

    $ sudo /etc/init.d/stunnel4 start

Clients on our network can now connect to Redis over SSL!

Hosting Flower
--------------

text here

Setting up Rollbar error tracking
---------------------------------

text here

Setting up Papertrail log management
------------------------------------

text here

Final thoughts
--------------

herp derp optimization

Footnotes
---------

.. Footnotes
.. [#aws-traffic] See https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html for instructions on opening EC2 instance ports.
.. [#stunnel-reference] The instructions for securing Redis with stunnel
   are adapted from
   https://redislabs.com/blog/stunnel-secure-redis-ssl/.
.. [#stunnel-better-way] Is there a better way of doing this, maybe with
   nginx? If you know a better way, please raise an issue at
   https://github.com/mwiens91/saltant/issues.

.. Links
.. _AWS EC2: https://aws.amazon.com/ec2/
.. _AWS Route 53: https://aws.amazon.com/route53/
.. _EFF Certbot: https://certbot.eff.org/
.. _Let's Encrypt: https://letsencrypt.org/
.. _nginx: https://www.nginx.com/
.. _stunnel: https://www.stunnel.org/
.. _systemd: https://freedesktop.org/wiki/Software/systemd/
.. _these routing instructions: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html
.. _these uWSGI and nginx instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
.. _these uWSGI Emperor vassal instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#configuring-uwsgi-to-run-with-a-ini-file
.. _uWSGI: https://github.com/unbit/uwsgi
.. _uWSGI Emperor: https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html
