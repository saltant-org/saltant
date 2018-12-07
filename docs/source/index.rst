Welcome to saltant!
===================

saltant is a web app for running task instances which are distributed
(run on many machines), containerized (run within `Docker`_ or
`Singularity`_ containers), and mutable (change often).

To accomplish this, saltant uses a few main pieces of tech:

- `Celery`_, a distributed task queue
- `Django`_, a web framework
- `Django REST framework`_, a RESTful API framework for Django
- `Docker`_, a containerization framework
- `PostgreSQL`_, an object-relational database server
- `RabbitMQ`_, a messaging broker
- `Singularity`_, another containerization framework

The source code for saltant is located at `github.com/saltant-org/saltant`_
and is licensed under the `MIT License`_. Additionally, a saltant API
reference is available at `saltant-org.github.io/saltant`_.

See also:

- `saltant-cli`_, a saltant CLI
- `saltant-py`_, a saltant SDK for Python

.. toctree::
   :maxdepth: 2
   :caption: Using saltant

   using/overview
   using/api-usage
   using/celery-workers
   using/working-example

.. toctree::
   :maxdepth: 2
   :caption: Hosting saltant

   hosting/introduction
   hosting/development
   hosting/production

.. Links to dependencies
.. _Celery: http://www.celeryproject.org/
.. _Django: https://www.djangoproject.com/
.. _Django REST Framework: http://www.django-rest-framework.org/
.. _Docker: https://www.docker.com/
.. _PostgreSQL: https://www.postgresql.org/
.. _RabbitMQ: https://www.rabbitmq.com/
.. _saltant-cli: https://github.com/saltant-org/saltant-cli/
.. _saltant-py: https://github.com/saltant-org/saltant-py/
.. _Singularity: https://www.sylabs.io/

.. Links to licenses
.. _MIT License: https://opensource.org/licenses/MIT

.. Other links
.. _github.com/saltant-org/saltant: https://github.com/saltant-org/saltant/
.. _saltant-org.github.io/saltant: https://saltant-org.github.io/saltant/
