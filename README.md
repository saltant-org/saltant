[![Build Status](https://travis-ci.com/mwiens91/saltant.svg?branch=master)](https://travis-ci.com/mwiens91/saltant)
[![codecov](https://codecov.io/gh/mwiens91/saltant/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/saltant)
[![Documentation Status](https://readthedocs.org/projects/saltant/badge/?version=latest)](https://saltant.readthedocs.io/en/latest/?badge=latest)
[![Python version](https://img.shields.io/badge/python-3.5%20|%203.6%20|%203.7-blue.svg)](https://github.com/mwiens91/saltant)

# saltant

### NOTE: this project is an active work in progress

saltant is a Django-powered web app for running task instances which are
distributed (run on many machines), containerized (run within
[Docker](https://www.docker.com/) or
[Singularity](https://www.sylabs.io/) containers), and mutable (change
often). You can find documentation for saltant at
[saltant.readthedocs.io](https://saltant.readthedocs.io/en/latest/).

saltant currently runs as a stand-alone application. However, with
minimal effort, saltant's main functionality can be refactored into an
app to be used within an existing Django project. Please raise an issue
if you are interested in isolating saltant as an independent app, and
we'll make it happen :smile:.

## Overview

saltant revolves around four main concepts: containers (which are
optional but recommended), task types, task queues, and task instances.
Containers contain code to run; task types specify a container (or
executable) and a set of variables/arguments required to run its code;
task queues specify a set of machines sharing similar environments which
run [Celery](https://github.com/celery/celery) workers; and task
instances specify a task type, provide the task type with its required
variables and arguments, and run its task type's container (or
executable) on a task queue.

While reading through the overview, it might be helpful to browse
saltant's API reference at
[mwiens91.github.io/saltant](https://mwiens91.github.io/saltant/).

### Containers

Containers are where your actual code is executed. If you don't know
what a container is, read [this](https://www.docker.com/what-container).

Containers in saltant are either Docker or Singularity containers.
Inside of each Container, you must have

+ a script to execute (more on this in the next paragraph)

and may optionally have

+ a set of environment variables consumed from the host machine
+ a directory to store logs
+ a directory to store results

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable :open_mouth:; (2) the script to
execute must take a JSON string (which encodes a set of arguments) as
its sole positional argument.

#### An alternative: executables

As an alternative to containers, you may instead use an executable
command which makes sense on the environments it is running on. Like the
executable script for containers, executables run directly must accept a
single JSON string containing all of its arguments.

### Task types

Task types name a container (or executable), constraints for the task's
environment, and what arguments must be provided to the task.
Specifically, a task type defines

#### Container tasks

+ a container image
+ a path to an executable script inside the container
+ a set of environment variables to consume from the host machine
+ a set of argument names for which task instances must provide values
+ a set of default values for the above argument names
+ a path to the logs directory inside the container (should one exist)
+ a path to the results directory inside the container (should one exist)

#### Executable tasks

+ a command to run
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
saltant server, both Python 2.x and 3.x are supported; workers will
additionally need to have Docker or Singularity binaries set up and
ready to run. Singularity >= 2.4 is required for Singularity container
use. Any recent version of Docker should be fine.

saltant requires a [RabbitMQ](https://www.rabbitmq.com/) messaging queue
to run its Celery queues and a [PostgreSQL](https://www.postgresql.org/)
database to store its data. It has optional support for the
[Flower](https://github.com/mher/flower) Celery web monitor.

saltant also integrates with two web services: it has optional support
for the [Rollbar](https://rollbar.com/) error tracking service, and
recommends using [Papertrail](https://paptertrailapp.com/) for log
management. Note that both Rollbar and Papertrail have generous free
tiers; see their respective sites for details.

## Is this secure?

saltant can have pretty much every aspect of its infrastructure secured
with SSL. Instructions for setting up a secure production server can be
found in the docs.
