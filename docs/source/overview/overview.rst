Overview
========

saltant revolves around four main concepts: containers, task types, task
queues, and task instances. Containers contain code to run; task types
specify a container and a set of variables required to run its code;
task queues specify a set of machines which share similar environments;
and task instances specify a task type, provide the task type with its
required variables, and run its task type's container on one of a task
queue's machines.

Containers
----------

Containers are where your actual code is executed. If you don't know
what a container is, read `this
<https://www.docker.com/what-container>`_.

Containers in saltant are either Docker or Singularity containers.
Inside of each Container, you must have

+ a script to execute (more on this next)
+ a set of environment variables consumed from the host
+ a set of directories bound to host directories for reading or writing
+ a directory bound to a host directory for streaming logs

Additionally, the aforementioned script must satisfy two criteria: (1)
the script to execute must be executable; (2) the script to execute must
take a JSON string (which encodes a set of arguments) as its sole
positional argument.

Task types
----------

Task types name a container, constraints for the container's
environment, and what arguments must be provided to the code inside of
the container.  Specifically, a task type defines

- a container image
- a path to an executable script inside of the container
- a set of environment variables to consume from the host machine
- a set of argument names for which task instances must provide values
- a set of default values for the above argument names
- a set of directories on the host machine to bind to directories within
  the container

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
