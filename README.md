[![Build Status](https://travis-ci.com/saltant-org/saltant.svg?branch=master)](https://travis-ci.com/saltant-org/saltant)
[![codecov](https://codecov.io/gh/saltant-org/saltant/branch/master/graph/badge.svg)](https://codecov.io/gh/saltant-org/saltant)
[![Documentation Status](https://readthedocs.org/projects/saltant/badge/?version=latest)](https://saltant.readthedocs.io/en/latest/?badge=latest)
[![Python version](https://img.shields.io/badge/python-3.5%20|%203.6%20|%203.7-blue.svg)](https://github.com/saltant-org/saltant)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# saltant

saltant is a Django-powered web app for running task instances which are
distributed (run on many machines), containerized (run within
[Docker](https://www.docker.com/) or
[Singularity](https://www.sylabs.io/) containers), and mutable (change
often). You can find documentation for saltant at
[saltant.readthedocs.io](https://saltant.readthedocs.io/en/latest/).

## Overview

saltant revolves around four main concepts: containers (which are
optional but recommended), task types, task queues, and task instances.
Containers contain code to run within an appropriate environment; task
types specify (optionally) a container, a base command to run, and a set
of variables/arguments to use; task queues specify sets of machines
running [Celery](https://github.com/celery/celery) workers; and task
instances specify a task type, provide the task type with its required
variables/arguments, and run its task type on a task queue.

While reading through the overview, it might be helpful to browse
saltant's API reference at
[saltant-org.github.io/saltant](https://saltant-org.github.io/saltant/).

### Containers

Containers are where your actual code is executed. If you don't know
what a container is, read [this](https://www.docker.com/what-container).

Containers in saltant are either Docker or Singularity containers.
Inside of each container, you must have

+ a script to execute (more on this in the next paragraph)

and may optionally have

+ a directory to store logs
+ a directory to store results

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable :open_mouth:; (2) the script to
execute must accept JSON encoding the task instance's set of arguments.

#### An alternative: "direct" executables

As an alternative to containers, you may instead run an executable
outside of a container. This is not recommended as managing environments
is more difficult this way, but may be necessary due to system
constraints.

### Task types

Task types name a container (or just an executable), constraints for a
task queue's environment, and what variables/arguments a task instance
must provide values for. Specifically, a task type defines

#### Container tasks

+ a container image
+ a path to an executable script inside the container
+ a set of environment variables to consume from the host machine
+ a set of argument names for which task instances must provide values
+ a set of default values for the above argument names
+ a path to the logs directory inside the container (should one exist)
+ a path to the results directory inside the container (should one exist)

#### Executable tasks

+ an executable command to run
+ a set of environment variables to consume from the host machine
+ a set of argument names for which task instances must provide values
+ a set of default values for the above argument names

### Task queues

Task queues specify a set of machines listening for new task instances
to consume. Machines in task queues must guarantee appropriate
environments for the set of task types being run on them.

### Task instances

Task instances name a task type to instantiate and a task queue to run
on. In addition, they provide the values for the required arguments of
the task type.

## What do I need?

saltant supports Python >= 3.5, although it may still run fine on
earlier Python 3.x versions. For
[Celery](https://github.com/celery/celery) workers connecting to a
saltant server, both Python 2.7 and >= 3.5 are supported; for running
container tasks, workers will additionally need to have Docker or
Singularity binaries set up and ready to run. Singularity >= 2.4 is
required for Singularity container use. Any recent version of Docker
should be fine.

saltant requires a [RabbitMQ](https://www.rabbitmq.com/) messaging queue
to run its Celery queues and a [PostgreSQL](https://www.postgresql.org/)
database to store its data. It has optional support for the
[Flower](https://github.com/mher/flower) Celery web monitor.

saltant optionally integrates with the [Rollbar](https://rollbar.com/)
error tracking service.

## Is this secure?

saltant can have pretty much every aspect of its infrastructure secured
with SSL. Instructions for setting up a secure production server can be
found in the docs.

## See also

+ [saltant-cli](https://github.com/saltant-org/saltant-cli/), a saltant CLI
+ [saltant-py](https://github.com/saltant-org/saltant-py/), a saltant SDK
  for Python
