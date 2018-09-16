Overview
========

saltant revolves around four main concepts: containers (which are
optional but recommended), task types, task queues, and task instances.
Containers contain code to run; task types specify a container (or
executable) and a set of variables/arguments required to run its code;
task queues specify a set of machines sharing similar environments which
run `Celery`_ workers; and task instances specify a task type, provide
the task type with its required variables and arguments, and run its
task type's container (or executable) on a task queue.

Containers
----------

Containers are where your actual code is executed. If you don't know
what a container is, read `this
<https://www.docker.com/what-container>`_.

Containers in saltant are either Docker or Singularity containers.
Inside of each Container, you must have

+ a script to execute (more on this in the next paragraph)

and may optionally have

+ a set of environment variables consumed from the host machine
+ a directory to store logs
+ a directory to store results

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable; (2) the script to execute must
take a JSON string (which encodes a set of arguments) as its sole
positional argument.

**An alternative: executables**

As an alternative to containers, you may instead use an executable
command which makes sense on the environments it is running on. Like the
executable script for containers, executables run directly must accept a
single JSON string containing all of its arguments.

Task types
----------

Task types name a container (or executable), constraints for the task's
environment, and what arguments must be provided to the task.
Specifically, a task type defines

**Container tasks**

+ a container image
+ a path to an executable script inside the container
+ a set of environment variables to consume from the host machine
+ a set of argument names for which task instances must provide values
+ a set of default values for the above argument names
+ a path to the logs directory inside the container (should one exist)
+ a path to the results directory inside the container (should one exist)

**Executable tasks**

+ a command to run
+ a set of environment variables to consume from the host machine
+ a set of argument names for which task instances must provide values
+ a set of default values for the above argument names

Task queues
-----------

Task queues specify a set of machines listening for new task instances
to consume. Machines in task queues must guarantee appropriate
environments for the set of task types being run on them.

Task instances
--------------

Task instances name a task type to instantiate and a task queue to run
on. In addition, they provide the values for the required arguments of
the task type.

.. Links
.. _Celery: http://www.celeryproject.org/
