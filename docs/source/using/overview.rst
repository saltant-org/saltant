Overview
========

saltant revolves around four main concepts: containers (which are
optional but recommended), task types, task queues, and task instances.
Containers contain code to run within an appropriate environment; task
types specify (optionally) a container, a base command to run, and a set
of variables/arguments to use; task queues specify sets of machines
running `Celery`_ workers; and task instances specify a task type,
provide the task type with its required variables/arguments, and run its
task type on a task queue.

While reading through the overview, it might be helpful to browse
saltant's API reference at `saltant-org.github.io/saltant`_.

Containers
----------

Containers are where your actual code is executed. If you don't know
what a container is, read `this
<https://www.docker.com/what-container>`_.

Containers in saltant are either `Docker`_ or `Singularity`_ containers.
Inside of each container, you must have

+ a script to execute (more on this in the next paragraph)

and may optionally have

+ a directory to store logs
+ a directory to store results

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable; (2) the script to execute must
accept JSON encoding the task instance's set of arguments.

**An alternative: "direct" executables**

As an alternative to containers, you may instead run an executable
outside of a container. This is not recommended as managing environments
is more difficult this way, but may be necessary due to system
constraints.

Task types
----------

Task types name a container (or just an executable), constraints for a
task queue's environment, and what variables/arguments a task instance
must provide values for. Specifically, a task type defines

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
.. _Docker: https://www.docker.com/
.. _Singularity: https://www.sylabs.io/
.. _saltant-org.github.io/saltant: https://saltant-org.github.io/saltant/
