A working example
=================

In this example we'll go over a simple example for how you might use
saltant to run a task. To make HTTP requests to our saltant server,
we'll use `HTTPie`_, which is essentially `curl`_ but prettier and
probably a bit less powerful (but powerful enough for our purposes).

The code for this example can be found at
`github.com/saltant-org/saltant-working-example`_.

Objective
---------

We're a programmer for Anagram Inc., a fictional software company
specializing in anagrams, and our boss has instructed us to write an
anagram generating task for our company's saltant server.

The task must satify the following criteria: given a ``word`` argument,
which might be, for example, "binary", we must create a results file
``binary.txt`` that contains all one-word anagrams of "binary":

- binary
- brainy

An anagram generator
--------------------

Before diving into any saltant specific logic, we need to solve the
anagram problem. To find all anagrams of a word, we need something to
permute the letters of the word and something to verify that a
permutation represents an English word.

Let's use Python to write the task. To generate permutations we can use
the `permutations`_ function from the `itertools`_ library, which is
part of the Python Standard Library; and to verify that permutations are
English words we can use a set of all English words from the
`english-words`_ Python package on `PyPI`_.

The following code does the job:

.. code-block:: python

    #!/usr/bin/env python3
    """Find anagrams of words."""

    from itertools import permutations
    from typing import Set
    from english_words import english_words_lower_alpha_set


    def find_anagrams(word: str) -> Set[str]:
        """Find all one-word anagrams of a word.
        Arg:
            word: a string containing a word to find anagrams of.
        Returns:
            A set containing all anagrams of the word, in lowercase. This is
            guaranteed to at least contain the word itself, provided the
            word passed in is an English word.
        """
        # Find all permutations of the word
        perms = {''.join(p) for p in permutations(word.lower())}

        # Filter out all non-English permutations
        anagrams = {word for word in perms
                    if word in english_words_lower_alpha_set}

        # Return the results
        return anagrams

We still haven't dealt with input arguments and saved our results to an
output file. We'll get to that next.

Getting input arguments
-----------------------

For saltant tasks, arguments come in the form of JSON. That is, if your
script is called ``main.py``, your script will be called as in the
following:

.. code-block:: console

    $ ./main.py '{"arg1": "val1", "arg2": "val2"}'

where ``arg{1,2}`` are arguments and ``val{1,2}`` are their
corresponding values.

The general strategy is to get all the arguments at runtime with
something like

.. code-block:: python

    import json
    import sys


    if __name__ == '__main__':
        # Get the arguments as a JSON string
        raw_args = sys.argv[1]

        # Parse the raw JSON and return a dictionary of the parsed
        # arguments
        args = json.loads(raw_args)

Now all of the arguments we need are in ``args``. Additionally, we can
do any validation we need to ensure that the values in ``args`` are
okay (but let's not worry about that here).

Tying this into our anagram example, our code becomes

.. code-block:: python

    #!/usr/bin/env python3
    """Find anagrams of words."""

    from itertools import permutations
    import json
    import sys
    from typing import Set
    from english_words import english_words_lower_alpha_set


    def find_anagrams(word: str) -> Set[str]:
        """Find all one-word anagrams of a word.

        Arg:
            word: a string containing a word to find anagrams of.
        Returns:
            A set containing all anagrams of the word, in lowercase. This is
            guaranteed to at least contain the word itself, provided the
            word passed in is an English word.

        """
        # Find all permutations of the word
        perms = {''.join(p) for p in permutations(word.lower())}

        # Filter out all non-English permutations
        anagrams = {word for word in perms
                    if word in english_words_lower_alpha_set}

        # Return the results
        return anagrams


    if __name__ == '__main__':
        # Get the arguments as a raw JSON string
        raw_args = sys.argv[1]

        # Parse the raw JSON and return a dictionary of the parsed
        # arguments
        args = json.loads(raw_args)

        # Find anagrams
        results = find_anagrams(args['word'])

Notice that we're making the assumption that ``word`` is going to be
passed into the JSON arguments; we will enforce this assumption when we
register our task to our saltant server.

Containerizing our code
-----------------------

The next obvious step is to save our anagram results somewhere. Where
will we put them? Well, eventually they're going to need to end up in a
container, so we might as well define our container first.

Inside of our container we need to make sure the following constraints
are satisfied:

#. All necessary Python requirements are installed
#. We have somewhere to put our results
#. We have somewhere to put our logs

To satisfy the first requirement we need a (Python) requirements file,
which will contain the following::

    english-words==1.0.1

since the english-words package is our only dependency outside of the
Python Standard Library.

At this point we have two files:

- ``main.py`` contains our anagram code
- ``requirements.txt`` contains our Python requirements

Before we define our containers, make sure that ``main.py`` is
executable:

.. code-block:: console

    $ chmod +x main.py

saltant needs its entry point to be executable, which is now taken care
of.

Defining a Docker container
---------------------------

Now let's package our code into a Docker container, keeping in mind our
requirements above. (We'll do the same thing but with a Singularity
container later.) Our ``Dockerfile`` might look like the following:

.. code-block:: docker

    # Use an official Python runtime as a parent image
    FROM python:3-slim

    # Set the working directory to /app
    WORKDIR /app

    # Copy the current directory contents into the container in its /app/
    # directory
    ADD main.py requirements.txt /app/

    # Install Python requirements
    RUN pip install -r requirements.txt

    # Logs can be collected here
    RUN mkdir /logs

    # Results can be collected here
    RUN mkdir /results

We can build this recipe and push it to `Docker Hub`_ (I'm using my user
for convenience here) with

.. code-block:: console

    $ docker build -t saltant/saltant-working-example .
    $ docker push saltant/saltant-working-example

or we can set up automated builds from a Git repository (which has been
set up for the source code for this example at
`github.com/saltant-org/saltant-working-example`_).

Defining a Singularity container
--------------------------------

Now we'll repeat the previous section, but use a Singularity container
instead of a Docker container. Our ``Singularity`` file might look like
the following::

    # Pull from Ubuntu 16.04 image
    Bootstrap: debootstrap
    OSVersion: xenial
    MirrorURL: http://us.archive.ubuntu.com/ubuntu/

    # Copy over files
    %files
        main.py /
        requirements.txt /

    %post
        # Create a directory to hold our scripts
        mkdir /app
        mv /main.py /app/
        mv /requirements.txt /app/

        # Make logs and results directories
        mkdir /logs
        mkdir /results

        # Install Python 3.5 and Pip
        apt-get install -y software-properties-common
        apt-add-repository universe
        apt-get update
        apt-get install -y python3-pip

        # Install Python requirements
        pip3 install -r /app/requirements.txt

Unlike Docker with Docker Hub, the only way to get Singularity images on
`Singularity Hub`_ is to use automated builds from a Git repository on
`GitHub`_ or `Bitbucket`_. To set up automated builds with Singularity
Hub, follow the instructions at
`github.com/singularityhub/singularityhub.github.io/wiki`_.

Saving anagram results
----------------------

At this point, we have put code in Docker and Singularity containers,
which, in my case, are located at

+ Docker Hub: `hub.docker.com/r/saltant/saltant-working-example/`_
+ Singularity Hub: `singularity-hub.org/collections/1444`_

However, we still haven't saved our results! Let's use the ``/results/``
directories we've created in our containers in our Python code:

.. code-block:: python

    #!/usr/bin/env python3
    """Find anagrams of words."""

    from itertools import permutations
    import json
    import os
    import sys
    from typing import Set
    from english_words import english_words_lower_alpha_set

    RESULTS_DIR = '/results/'


    def find_anagrams(word: str) -> Set[str]:
        """Find all one-word anagrams of a word.

        Arg:
            word: a string containing a word to find anagrams of.
        Returns:
            A set containing all anagrams of the word, in lowercase. This is
            guaranteed to at least contain the word itself, provided the
            word passed in is an English word.

        """
        # Find all permutations of the word
        perms = {''.join(p) for p in permutations(word.lower())}

        # Filter out all non-English permutations
        anagrams = {word for word in perms
                    if word in english_words_lower_alpha_set}

        # Return the results
        return anagrams


    if __name__ == '__main__':
        # Get the arguments as a raw JSON string
        raw_args = sys.argv[1]

        # Parse the raw JSON and return a dictionary of the parsed
        # arguments
        args = json.loads(raw_args)
        word = args['word']

        # Save anagrams
        filename = os.path.join(
            RESULTS_DIR,
            word + '.txt')

        with open(filename, 'w') as f:
            for result in find_anagrams(word):
                f.write(result + '\n')

Great! Before we register our task, we should add some basic logging so
that debugging is easier down the line should we run into problems.

Logging the saltant way
-----------------------

Now let's log some basic information to a file using Python's `logging`_
library. All we need to do is log to a file in the directory that we've
set up for our logs, ``/logs/``. Let's make use of the environment
variables ``JOB_UUID``, which is a variable containing the UUID of the
task instance, passed down to every saltant-instantiated container and
put all of the logs in ``logs/JOB_UUID-logs.txt``.

The following code shows some toy debugging messages along with the
logger setup:

.. code-block:: python

    #!/usr/bin/env python3
    """Find anagrams of words."""

    from itertools import permutations
    import json
    import logging
    import os
    import sys
    from typing import Set
    from english_words import english_words_lower_alpha_set

    LOGS_DIR = '/logs/'
    RESULTS_DIR = '/results/'


    def find_anagrams(word: str) -> Set[str]:
        """Find all one-word anagrams of a word.

        Arg:
            word: a string containing a word to find anagrams of.
        Returns:
            A set containing all anagrams of the word, in lowercase. This is
            guaranteed to at least contain the word itself, provided the
            word passed in is an English word.

        """
        # Find all permutations of the word
        logging.debug("Obtaining all permutations for \"%s\"", word)
        perms = {''.join(p) for p in permutations(word.lower())}

        # Filter out all non-English permutations
        logging.debug("Filtering all permutations for \"%s\"", word)
        anagrams = {word for word in perms
                    if word in english_words_lower_alpha_set}

        # Return the results
        return anagrams


    if __name__ == '__main__':
        # Set up the logger
        uuid = os.environ['JOB_UUID']
        logs_path = os.path.join(
            LOGS_DIR,
            uuid + '-logs.txt')

        logging.basicConfig(
            filename=logs_path,
            level=logging.DEBUG,
            format='%(levelname)s: %(message)s')

        # Get the arguments as a raw JSON string
        raw_args = sys.argv[1]

        # Parse the raw JSON and return a dictionary of the parsed
        # arguments
        args = json.loads(raw_args)
        word = args['word']

        # Save anagrams
        results_path = os.path.join(
            RESULTS_DIR,
            word + '.txt')

        with open(results_path, 'w') as f:
            for result in find_anagrams(word):
                f.write(result + '\n')

POST-ing the task to our saltant server
---------------------------------------

Now all of the coding we need to do is done. What's left is to make a
couple of requests to our saltant server, and we're set.

For the purposes of this documentation let's suppose our saltant server
is set up up at ``https://www.anagraminc.org/saltant/`` and that our API
token for it is ``p0gch4mp101fy451do9uod1s1x9i4a``.

To register our task we'll hit the `/containertasktypes/`_ API endpoint
with information about our task (we'll use the Singularity image here
instead of the Docker image):

.. code-block:: console

    $ http POST "https://www.anagraminc.org/saltant/api/containertasktypes/" \
        name="anagram-generator" \
        description="Generates anagrams of a given word." \
        container_image="shub://saltant-org/saltant-working-example" \
        container_type="singularity" \
        script_path="/app/main.py" \
        logs_path="/logs/" \
        results_path="/results/" \
        required_arguments:='["word"]' \
        "Authorization: Token p0gch4mp101fy451do9uod1s1x9i4a"

and we should get back a response that looks like

.. code-block:: http

    HTTP/1.1 201 Created
    Allow: GET, POST
    Content-Length: 415
    Content-Type: application/json
    Date: Thu, 16 Aug 2018 01:27:08 GMT
    Server: WSGIServer/0.2 CPython/3.6.5
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "container_image": "shub://saltant-org/saltant-working-example",
        "container_type": "singularity",
        "datetime_created": "2018-08-16T01:27:08.766216Z",
        "description": "Generates anagrams of a given word.",
        "environment_variables": [],
        "id": 11,
        "logs_path": "/logs/",
        "name": "anagram-generator",
        "required_arguments": [
            "word"
        ],
        "required_arguments_default_values": {},
        "results_path": "/results/",
        "script_path": "/app/main.py",
        "user": "matt"
    }

Running the task
----------------

Our boss has told us that we should run our task on his saltant task
queue ``anagram-queue``, which he has told us has ID ``4``. To do this,
we make another request (this time to `/containertaskinstances/`_),
keeping in mind the ID of the task type we just created (which is
``11``):

.. code-block:: console

    $ http POST "https://www.anagraminc.org/saltant/api/containertaskinstances/" \
        arguments:='{"word": "binary"}' \
        task_type=11 \
        task_queue=4 \
        "Authorization: Token p0gch4mp101fy451do9uod1s1x9i4a"

to which we should get a response like

.. code-block:: http

    HTTP/1.1 201 Created
    Allow: GET, POST
    Content-Length: 223
    Content-Type: application/json
    Date: Thu, 16 Aug 2018 01:29:38 GMT
    Server: WSGIServer/0.2 CPython/3.6.5
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "arguments": {
            "word": "binary"
        },
        "datetime_created": "2018-08-16T17:30:59.634727Z",
        "datetime_finished": null,
        "name": "",
        "state": "created",
        "task_queue": 4,
        "task_type": 11,
        "user": "matt",
        "uuid": "0b9715ff-df56-4331-9ba0-48597ae1f832"
    }

The logs and results should now be available at the logs and results
directories specified by the worker that ran the task on our boss' task
queue. The logs will be made available to the saltant front-end, but the
results will stay on the worker's machine.

Addendum: filesystem interfacing with Singularity
-------------------------------------------------

When we made a request to create our task type, as in

.. code-block:: console

    $ http POST "https://www.anagraminc.org/saltant/api/containertasktypes/" \
        name="anagram-generator" \
        description="Generates anagrams of a given word." \
        container_image="shub://saltant-org/saltant-working-example" \
        container_type="singularity" \
        script_path="/app/main.py" \
        logs_path="/logs/" \
        results_path="/results/" \
        required_arguments:='["word"]' \
        "Authorization: Token p0gch4mp101fy451do9uod1s1x9i4a"

The ``logs_path`` and ``results_path`` specify where in the container
saltant should bind the worker's ``WORKER_LOGS_DIRECTORY`` and
``WORKER_RESULTS_DIRECTORY``. However, even somewhat recent-ish versions
of Singularity have problems with custom bind points: they're (so far as
I'm aware) basically guaranteed to work with Singularity 2.4, but that
was only released on 2017-10-02, and on earlier versions they *might*
work (but no promises).

This may be a problem. Unless you can convince your system administrator
to upgrade to Singularity 2.4, you'll need a workaround.

One workaround works only if Singularity mounts the host's filesystem to
its images. In this case, the play is to, instead of making a request as
bove, to not specify the ``logs_path`` and ``results_path`` and instead
consume the worker's ``WORKER_LOGS_DIRECTORY`` and
``WORKER_RESULTS_DIRECTORY`` environment variables and use those
directly in your script.

So, for example, in ``main.py`` we might make the following changes:

.. code-block:: python

    #!/usr/bin/env python3
    """Find anagrams of words."""

    from itertools import permutations
    import json
    import logging
    import os
    import sys
    from typing import Set
    from english_words import english_words_lower_alpha_set

    LOGS_DIR = os.path.join(
        os.environ['WORKER_LOGS_DIRECTORY'],
        os.environ['JOB_UUID'])
    RESULTS_DIR = os.path.join(
        os.environ['WORKER_RESULTS_DIRECTORY'],
        os.environ['JOB_UUID'])


    def find_anagrams(word: str) -> Set[str]:
        """Find all one-word anagrams of a word.

        Arg:
            word: a string containing a word to find anagrams of.
        Returns:
            A set containing all anagrams of the word, in lowercase. This is
            guaranteed to at least contain the word itself, provided the
            word passed in is an English word.

        """
        # Find all permutations of the word
        logging.debug("Obtaining all permutations for \"%s\"", word)
        perms = {''.join(p) for p in permutations(word.lower())}

        # Filter out all non-English permutations
        logging.debug("Filtering all permutations for \"%s\"", word)
        anagrams = {word for word in perms
                    if word in english_words_lower_alpha_set}

        # Return the results
        return anagrams


    if __name__ == '__main__':
        # Set up the logger
        uuid = os.environ['JOB_UUID']
        logs_path = os.path.join(
            LOGS_DIR,
            uuid + '-logs.txt')

        logging.basicConfig(
            filename=logs_path,
            level=logging.DEBUG,
            format='%(levelname)s: %(message)s')

        # Get the arguments as a raw JSON string
        raw_args = sys.argv[1]

        # Parse the raw JSON and return a dictionary of the parsed
        # arguments
        args = json.loads(raw_args)
        word = args['word']

        # Save anagrams
        results_path = os.path.join(
            RESULTS_DIR,
            word + '.txt')

        with open(results_path, 'w') as f:
            for result in find_anagrams(word):
                f.write(result + '\n')

Note that, in the usual case when you specify non-null values for
``logs_path`` and ``results_path`` in the request, the logs and results
are placed in a subdirectory that is named based on the task instance's
UUID, which we've emulated in the code above.

And then our request to create the task type would instead look like

.. code-block:: console

    $ http POST "https://www.anagraminc.org/saltant/api/tasktypes/" \
        name="anagram-generator" \
        description="Generates anagrams of a given word." \
        container_image="shub://saltant-org/saltant-working-example" \
        container_type="singularity" \
        script_path="/app/main.py" \
        environment_variables:='["WORKER_LOGS_DIRECTORY", "WORKER_RESULTS_DIRECTORY"]' \
        required_arguments:='["word"]' \
        "Authorization: Token p0gch4mp101fy451do9uod1s1x9i4a"

.. Links
.. _Bitbucket: https://bitbucket.org/
.. _curl: https://curl.haxx.se/
.. _Docker Hub: https://hub.docker.com/
.. _english-words: https://pypi.org/project/english-words/
.. _GitHub: https://github.com/
.. _HTTPie: https://httpie.org/
.. _itertools: https://docs.python.org/3/library/itertools.html
.. _logging: https://docs.python.org/3/library/logging.html
.. _permutations: https://docs.python.org/3/library/itertools.html#itertools.permutations
.. _PyPI: https://pypi.org/
.. _Singularity Hub: https://singularity-hub.org/

.. Long links
.. _github.com/saltant-org/saltant-working-example: https://github.com/saltant-org/saltant-working-example
.. _github.com/singularityhub/singularityhub.github.io/wiki: https://github.com/singularityhub/singularityhub.github.io/wiki
.. _hub.docker.com/r/saltant/saltant-working-example/: https://hub.docker.com/r/saltant/saltant-working-example/
.. _singularity-hub.org/collections/1444: https://singularity-hub.org/collections/1444

.. API endpoint links
.. _/containertaskinstances/: https://saltant-org.github.io/saltant/#operation/containertaskinstances_create
.. _/containertasktypes/: https://saltant-org.github.io/saltant/#operation/containertasktypes_create
