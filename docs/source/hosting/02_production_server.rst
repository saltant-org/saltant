Hosting a production server
===========================

How you set up a production server really depends on your setup. One way
is to host saltant with uWSGI and nginx, following this wonderful guide:

    https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

There are a few things that *really* should be done:

Django checklist
----------------

+ Make sure DEBUG is False
+ Make sure you've generated a unique SECRET_KEY
+ Make sure you're using SSL

redis setup
-----------

stuff

flower setup
------------

god this is painful

logs w/papertrail setup
-----------------------

stuff

launching more workers
----------------------

yay
