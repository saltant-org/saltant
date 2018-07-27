Welcome to saltant!
===================

saltant is a web app for running task instances which are distributed
(run on many machines), containerized (run within `Docker`_ or
`Singularity`_ containers), and mutable (change often).

To accomplish this, saltant uses lots of tech [#tech]_:

- `Celery`_ (`BSD-3-Clause License`_), a distributed task queue
- `Django`_ (`BSD-3-Clause License`_), a web framework
- `Django REST framework`_ (`BSD-3-Clause License`_), a RESTful API framework for Django
- `docker-py`_ (`Apache-2.0 License`_), Docker SDK for Python
- `Flower`_ (`BSD-3-Clause License`_), a web monitor for Celery
- `PostgreSQL`_ (`PostgreSQL License`_), an object-relational database server
- `RabbitMQ`_ (`MPL 1.1 License`_), a messaging broker
- `singularity-cli`_ (`GNU Affero General Public License v3.0 License`_), Singularity SDK for Python

And lots of services:

- `Papertrail`_, cloud-hosted log management
- `Rollbar`_, real-time error alerting and debugging tools

The source code for saltant is located `here
<https://github.com/mwiens91/saltant>`_ and is licensed under the `MIT
License`_.

.. toctree::
   :maxdepth: 1
   :caption: Overview

   overview/overview

.. toctree::
   :maxdepth: 1
   :caption: API Usage

   api/placeholder

.. toctree::
   :maxdepth: 1
   :caption: Running Celery Workers

   celery-workers/placeholder

.. toctree::
   :maxdepth: 1
   :caption: Hosting saltant

   hosting/introduction
   hosting/development
   hosting/production

.. Footnotes
.. [#tech] For brevity, only major direct dependencies are listed.

.. Links to dependencies
.. _Celery: http://www.celeryproject.org/
.. _Django: https://www.djangoproject.com/
.. _Django REST Framework: http://www.django-rest-framework.org/
.. _Docker: https://www.docker.com/
.. _docker-py: https://github.com/docker/docker-py
.. _Flower: https://github.com/mher/flower
.. _PostgreSQL: https://www.postgresql.org/
.. _RabbitMQ: https://www.rabbitmq.com/
.. _Singularity: https://www.sylabs.io/
.. _singularity-cli: https://github.com/singularityhub/singularity-cli

.. Links to licenses
.. _Apache-2.0 License: https://www.apache.org/licenses/LICENSE-2.0
.. _BSD-3-Clause License: https://opensource.org/licenses/BSD-3-Clause
.. _GNU Affero General Public License v3.0 License: https://www.gnu.org/licenses/agpl.html
.. _MIT License: https://opensource.org/licenses/MIT
.. _MPL 1.1 License: https://www.mozilla.org/en-US/MPL/1.1/
.. _PostgreSQL License: https://www.postgresql.org/about/licence/

.. Links to services
.. _Papertrail: https://papertrailapp.com/
.. _Rollbar: https://rollbar.com/
