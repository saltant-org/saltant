Production server setup
=======================

.. highlight:: console

As mentioned in the :doc:`introduction <introduction>`, the steps you
need to setup a saltant production server are very sensitive to your
particular environment and implementation needs. Hence, for this section
of hosting instructions we will discuss *a* way to set up saltant in
production, not *the* way (and not necessarily even the "best" way).

Also note that production settings are finicky, and the packages
mentioned here may change their interface over time! Make you sure you
adapt any changes as necessary.

This section continues directly from the :doc:`development`
instructions.

Allowing incoming network traffic
---------------------------------

For simplicity, let's assume we are using `AWS Route 53`_ to route
traffic from our domain, ``www.fictionaljobrunner.com``, to an `AWS
EC2`_ instance used to host our saltant project, PostgreSQL database
server, and RabbitMQ server. These steps should translate over to most
implementation methods with (hopefully) minimal modification. We will
also assume that the PostgreSQL database server doesn't need to expose
itself to the network, and that the RabbitMQ server *does* need to
expose itself to the network.

Start by routing traffic from your domain to your EC2 instance by
following. Set up ALIAS DNS records for ``fictionaljobrunner.com`` and
``www.fictionaljobrunner.com``. You may find `these routing
instructions`_ helpful.

Now, make sure you have ports open for SSH (22), HTTP (80), HTTPS (443),
and AMQP (5671) traffic. [#aws-traffic]_ Later, we will redirect HTTP
requests to HTTPS in `Let's encrypt!`_, and secure incoming Redis
traffic with SSL in `Securing RabbitMQ with SSL`_.

Setting up production environment variables
-------------------------------------------

We'll need to fill in production values for a few of our environment
variables, namely ``ALLOWED_HOSTS`` and ``DJANGO_BASE_URL``. Assuming
that we've set up ALIAS DNS records for ``fictionaljobrunner.com`` and
``www.fictionaljobrunner.com`` in the previous step, the relevant
variables of our ``.env`` file might look like

.. code-block:: shell

    ALLOWED_HOSTS='fictionaljobrunner.com','www.fictionaljobrunner.com','127.0.0.1'
    DJANGO_BASE_URL='https://www.fictionaljobrunner.com'

Collecting static files
-----------------------

Before we host saltant, we need to collect all of our project's static
files so we can serve them efficiently. From the base of the project,
simply run ::

    $ ./manage.py collectstatic

Adding a logo and a favicon
---------------------------

Now is probably a good time to add a logo graphic and a favicon. Make
sure the logo graphic is in PNG format with a 1:1 aspect ratio. Replace
the default logo at ``static/splashpage/img/logo.png`` and the default
favicon at ``static/splashpage/favicon/favicon.ico`` with your own logo
image and favicon, respectively.

Hosting saltant on a socket with uWSGI
--------------------------------------

This and the next section are adapted from `these uWSGI and nginx
instructions`_, which provide a much more detailed reference for the
following instructions.

First we need to install `uWSGI`_; if we're on Ubuntu we can install
it with ::

    $ sudo pip3 install uwsgi

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
    ExecStart=/usr/local/bin/uwsgi --ini /etc/uwsgi/emperor.ini
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

To enable this site, we need create the following symlink so nginx
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

Hosting RabbitMQ on a network
-----------------------------

Now let's focus on RabbitMQ. If all of your Celery workers will be running
on the local machine, then you can safely ignore this section.

By default, RabbitMQ will bind to all interfaces, on IPv4 and IPv6 if
available. Let's suppose our IP is ``192.168.1.100``. The minimum amount
of work required to host RabbitMQ on a network is to change the
``CELERY_BROKER_URL`` in our ``.env`` from

.. code-block:: shell

    CELERY_BROKER_URL='pyamqp://'

to

.. code-block:: shell

    CELERY_BROKER_URL='pyamqp://192.168.1.100:5671'

But suppose we want some basic authentication. Let's include that now.
RabbitMQ comes with a default user ``guest`` (with password ``guest``)
and a default `virtual host`_ ``/``. Let's remove those::

    $ sudo rabbitmqctl delete_user guest
    $ sudo rabbitmqctl delete_vhost /

Now let's add our own admin user ``AzureDiamond`` (with password
``hunter2``) and virtual host ``AzureDiamond_vhost``::

    $ sudo rabbitmqctl add_user AzureDiamond hunter2
    $ sudo rabbitmqctl add_vhost AzureDiamond_vhost``
    $ sudo rabbitmqctl set_user_tags AzureDiamond administrator
    $ sudo rabbitmqctl set_permissions -p AzureDiamond_vhost AzureDiamond ".*" ".*" ".*"

Now that we've done this, we need to update the ``CELERY_BROKER_URL``
variable in our project's ``.env``:

.. code-block:: shell

    CELERY_BROKER_URL='pyamqp://AzureDiamond:hunter2@192.168.1.100:5671/AzureDiamond_vhost'

Hosting the RabbitMQ management console with SSL
------------------------------------------------

Our strategy here will be to host the RabbitMQ management console on
localhost and create a reverse proxy with nginx to expose to the
network. All we need to do is edit the
nginx saltant configuration again, and add two new locations within the
server block: [#rabbitmq-management-nginx]_

**/etc/nginx/sites-available/saltant_nginx.conf**

.. code-block:: nginx

    server {

        ... # stuff we added before (and that Certbot added to!)

        location ~* /rabbitmq/api/(.*?)/(.*) {
            proxy_pass http://localhost:15672/api/$1/%2F/$2?$query_string;
            proxy_buffering                    off;
            proxy_set_header Host              $http_host;
            proxy_set_header X-Real-IP         $remote_addr;
            proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location ~* /rabbitmq/(.*) {
            rewrite ^/rabbitmq/(.*)$ /$1 break;
            proxy_pass http://localhost:15672;
            proxy_buffering                    off;
            proxy_set_header Host              $http_host;
            proxy_set_header X-Real-IP         $remote_addr;
            proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

Now let's change the ``RABBITMQ_MANAGEMENT_URL`` in your ``.env`` to

.. code-block:: shell

    RABBITMQ_MANAGEMENT_URL='https://www.fictionaljobrunner.com/rabbitmq/'

Securing RabbitMQ with SSL
--------------------------

Even though we have secured the RabbitMQ management console with SSL,
RabbitMQ is still insecure. If you're hosting all of your workers on
a secure network, then feel free to skip this section.

We're going to make use of the certs we created in `Let's encrypt!`_.
Noting where those files are, create or edit the following file, like
so:

**/etc/rabbitmq/rabbitmq.config**

.. code-block:: erlang

    [
     {rabbit,
      [
       {tcp_listeners, []},
       {ssl_listeners, [5671]},
       {ssl_options, [{cacertfile,           "/etc/letsencrypt/live/fictionaljobrunner.com/fullchain.pem"},
                      {certfile,             "/etc/letsencrypt/live/fictionaljobrunner.com/cert.pem"},
                      {keyfile,              "/etc/letsencrypt/live/fictionaljobrunner.com/privkey.pem"},
                      {verify,               verify_peer},
                      {fail_if_no_peer_cert, false}]}
      ]
     }
    ].

Make sure that the ``rabbitmq`` user on your machine has read access to
the above certs. (One way to do this is to let the ``ssl-cert`` group
control ``/etc/letsencrypt`` and add ``rabbitmq`` to this group.)

Hosting Flower with SSL
-----------------------

Hosting Flower is simple with nginx. First let's daemonize Flower with
systemd (assuming our saltant virtual environment is located at
``/home/ubuntu/saltant/venv``:

**/etc/systemd/system/flower.service**

.. code-block:: ini

    [Unit]
    Description=Flower
    After=syslog.target

    [Service]
    WorkingDirectory=/home/ubuntu/saltant/
    ExecStart=/home/ubuntu/saltant/venv/bin/flower -A saltant --url-prefix=flower --basic_auth=AzureDiamond:hunter2 --db=flower.db --persistent=True
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

Just like in `Hosting saltant on a socket with uWSGI`_, we need to make
this service executable and enable it::

    $ sudo chmod +x /etc/systemd/system/flower.service
    $ sudo servicectl enable flower.service

Now we have Flower daemonized on our local machine with some basic
authentication [#flowerauth]_, but it's still not exposed to the network. To do so
we'll take the reverse proxy tack taken in `Hosting the RabbitMQ
management console with SSL`_. First, get the directory path for
Flower's static files (let's assume the path is
``/home/ubuntu/saltant/venv/lib/python3.6/site-packages/flower/static``;
your's should be similar). Then let's add the following two locations to
the server block in our nginx configuration file:

**/etc/nginx/sites-available/saltant_nginx.conf**

.. code-block:: nginx

    server {

        ... # stuff we added before (and that Certbot added to!)

        location /flower/static {
            alias /home/ubuntu/saltant/venv/lib/python3.6/site-packages/flower/static;
        }

        location /flower {
            proxy_pass http://localhost:5555/;
            rewrite ^/flower/(.*)$ /$1 break;
            proxy_set_header Host $host;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }

Now let's let saltant know about Flower. Change the ``FLOWER_URL``
variable in ``.env`` to

.. code-block:: shell

    FLOWER_URL='https://www.fictionaljobrunner.com/flower/'

Setting up Rollbar error tracking
---------------------------------

`Rollbar`_ provides a beautiful error-tracking solution for development
teams. It also has a generous free tier (yay!). You can sign up `here
<https://rollbar.com/signup/>`_.

Once you, have, fill in the ``ROLLBAR_ACCESS_TOKEN`` and
``ROLLBAR_PROJECT_URL`` variables in your ``.env``.

Setting up Papertrail log management
------------------------------------

`Papertrail`_ is beautiful log management system which also has a
generous free tier (double yay!). You can sign up `here
<https://papertrailapp.com/signup?plan=free>`_.

As of this writing, Papertrail's free tier only retains logs for 7 days;
however, you can link an `AWS S3`_ bucket for it to write archives to
nightly, effectively giving you unlimited retention.

Final thoughts
--------------

This guide has demonstrated one way you can host salant in production.
It covers basic security and it should work. However, there's a whole
world (well, industry) worth of extra security and optimization that can
be added on top of this to make saltant run better. Be aware of that.

.. Footnotes
.. [#aws-traffic] See `here <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html>`_ for instructions on opening EC2 instance ports.
.. [#rabbitmq-management-nginx] Thanks to Dario Zadro for his post `here <https://stackoverflow.com/questions/49742269/rabbitmq-management-over-https-and-nginx>`_.
.. [#flowerauth] See more authentication options `here <https://flower.readthedocs.io/en/latest/auth.html>`_.

.. Links
.. _amqp: https://amqp.readthedocs.io/en/latest/
.. _AWS EC2: https://aws.amazon.com/ec2/
.. _AWS Route 53: https://aws.amazon.com/route53/
.. _AWS S3: https://aws.amazon.com/s3/
.. _EFF Certbot: https://certbot.eff.org/
.. _Let's Encrypt: https://letsencrypt.org/
.. _librabbitmq: https://github.com/celery/librabbitmq/
.. _nginx: https://www.nginx.com/
.. _Papertrail: https://papertrailapp.com/
.. _Rollbar: https://rollbar.com/
.. _systemd: https://freedesktop.org/wiki/Software/systemd/
.. _these routing instructions: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html
.. _these uWSGI and nginx instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
.. _these uWSGI Emperor vassal instructions: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#configuring-uwsgi-to-run-with-a-ini-file
.. _uWSGI: https://github.com/unbit/uwsgi
.. _uWSGI Emperor: https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html
.. _virtual host: https://www.rabbitmq.com/vhosts.html
