[![Build Status](https://travis-ci.com/mwiens91/saltant.svg?branch=master)](https://travis-ci.com/mwiens91/saltant)
[![codecov](https://codecov.io/gh/mwiens91/saltant/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/saltant)
[![Documentation Status](https://readthedocs.org/projects/saltant/badge/?version=latest)](https://saltant.readthedocs.io/en/latest/?badge=latest)

# saltant

### NOTE: this project is an active work in progress

saltant is a web app for running task instances which are distibuted
(run on many machines), containerized (run within
[Docker](https://www.docker.com/) or
[Singularity](https://www.sylabs.io/) containers), and mutable (change
often). You can find documentation for saltant
[here](https://saltant.readthedocs.io/en/latest/).

## What do I need?

saltant supports Python >= 3.5, although it may still run fine on
earlier Python 3.x versions. Similar Python requirements hold for
[Celery](https://github.com/celery/celery) workers connecting to a
saltant server; although workers will additionally need to have Docker
or Singularity binaries set up and ready to run.

A messaging queue ([RabbitMQ](https://www.rabbitmq.com/) is recommended)
also needs to be run on a machine, whether the machine hosting saltant
or a different machine.

## Is this secure?

saltant can have pretty much every aspect of its infrastructure secured
with SSL. Instructions for setting up a secure production server can be
found in the docs.
