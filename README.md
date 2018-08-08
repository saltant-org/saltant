[![Build Status](https://travis-ci.com/mwiens91/saltant.svg?branch=master)](https://travis-ci.com/mwiens91/saltant)
[![codecov](https://codecov.io/gh/mwiens91/saltant/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/saltant)
[![Documentation Status](https://readthedocs.org/projects/saltant/badge/?version=latest)](https://saltant.readthedocs.io/en/latest/?badge=latest)

# saltant

### NOTE: this project is an active work in progress

saltant is a web app for running task instances which are distributed
(run on many machines), containerized (run within
[Docker](https://www.docker.com/) or
[Singularity](https://www.sylabs.io/) containers), and mutable (change
often). You can find documentation for saltant at
[saltant.readthedocs.io](https://saltant.readthedocs.io/en/latest/).

saltant is currently a stand-alone application. However, with minimal
effort, saltant's main functionality can be used within an existing
Django project. Please raise an issue if you are interested in isolating
saltant as an independent app for use within another Django project, and
we'll make it happen :smile:.

## Overview

saltant revolves around four main concepts: containers, task types, task
queues, and task instances. Containers contain code to run; task types
specify a container and a set of variables required to run its code;
task queues specify a set of machines which share similar environments;
and task instances specify a task type, provide the task type with its
required variables, and run its task type's container on one of a task
queue's machines.

While reading through the overview, it might be helpful to browse
saltant's API reference at
[mwiens91.github.io/saltant](https://mwiens91.github.io/saltant/).

### Containers

Containers are where your actual code is executed. If you don't know
what a container is, read [this](https://www.docker.com/what-container).

Containers in saltant are either Docker or Singularity containers.
Inside of each Container, you must have

+ a script to execute (more on this next)
+ a set of environment variables consumed from the host

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable :open_mouth:; (2) the script to
execute must take a JSON string (which encodes a set of arguments) as
its sole positional argument.

### Task types

Task types name a container, constraints for the container's
environment, and what arguments must be provided to the code inside of
the container.  Specifically, a task type defines

+ a container image
+ a path to an executable script inside the container
+ paths to the logs and results directories inside the container
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
