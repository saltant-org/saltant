Running Celery workers
======================

.. highlight:: console

Celery workers are the processes that consume and run task instances
from task queues. For general information on Celerys workers, see
`Celery's worker documentation`_.

Setup
-----

To run a worker you need to clone and configure a subset of the saltant
project on the machine you want to run jobs from.

First, clone the saltant repository and move into it::

    $ git clone https://github.com/mwiens91/saltant.git
    $ cd saltant

Next create a Python 3.x virtual environment for the worker, using your
prefered method, or with ::

    $ python3 -m venv venv
    $ source venv/bin/activate

To install the requirements for a worker, run ::

    $ pip install -r requirements-worker.txt

You'll also need to fill in a subset of saltant's required environment
variables. First, copy the example ``.env.example`` file to ``.env``::

    $ cp .env.example .env

Fill in the environment variables under the ``## Celery worker
environment - ... ##`` heading (you can ignore all environment variables
under the ``## Django environment - ... ##`` heading).

Note that at present you *need* a permanent authorization token to run
workers.

**Container support**

Your worker's machine should support at least one of Docker or
Singularity.

To install Singularity, see `Singularity's installation instructions`_.
However, if you're on Ubuntu, you can get away with ::

    $ sudo apt install singularity-container

To install Docker, see `Docker's installation instructions`_.

Starting a worker process
-------------------------

First make sure that you have a task queue available in the saltant
project appropriate for the worker you want to spawn; let's call this
task queue ``thistaskqueue``.

Then, to launch a worker process in your current shell, run ::

    $ celery worker -A saltant -Q thistaskqueue

Again, see `Celery's worker documentation`_ for more details. There are
also daemonization options for workers; for those, see `Celery's worker
daemon documentation`_.

.. Links
.. _Celery's worker documentation: http://docs.celeryproject.org/en/latest/userguide/workers.html
.. _Celery's worker daemon documentation: http://docs.celeryproject.org/en/latest/userguide/daemonizing.html
.. _Docker's installation instructions: https://docs.docker.com/install/
.. _Singularity's installation instructions: https://www.sylabs.io/guides/2.5.1/user-guide/installation.html
