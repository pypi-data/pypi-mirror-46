python-angreal
==============

An angreal for gitlab based python projects.


`init` :
---------

On initialization this angreal will create a python project. Optionally it will register the project
on pypi with a `0.0.0` release, and upload to a remote on `gitlab.com`.

.. code-block:: bash

    angreal init python-angreal [OPTIONS]

    Options:
      --gitlab_token TEXT  gitlab token to use (default = $GITLAB_TOKEN)
      --no_pypi            do not setup a pypi registry
      --no_gitlab          no gitlab project created






`bump`:
--------
Bumps the `VERSION` file.

.. code-block:: bash

     Usage: angreal bump [OPTIONS]

      bump the current package version

    Options:
      --major  Make a major bump (0.0.0 -> 1.0.0)
      --minor  Make a major bump (0.0.0 -> 0.1.0)
      --patch  Make a major bump (0.0.0 -> 0.0.1)
      --help   Show this message and exit.


`docs`:
--------

Generates the sphinx documentation for the project opening it in a new web browser.


.. code-block:: bash

   Usage: angreal docs [OPTIONS]

    compile documentation for the project

    Options:
      --no_open  Do not immediately open
      --help     Show this message and exit.

`integration`:
--------------

Run integration/functional tests on the current package. These tests are housed
within `tests/integration` and are for ensuring end to end operation of portions
of software.

.. code-block:: bash

    Usage: angreal integration [OPTIONS]

      run package tests

    Options:
      --help  Show this message and exit.

`setup`:
--------

Setup the package environment. Currently creates

.. code-block:: bash

    Usage: angreal setup [OPTIONS]

      update/create the package_name environment.

    Options:
      --no_dev  Don't setup a development environment.
      --help    Show this message and exit.


`tests`:
---------

Run tests on the current package.

.. code-block:: bash

    Usage: angreal tests [OPTIONS]

      run package tests

    Options:
      --html TEXT  generate an html report and open in a browser
      --help       Show this message and exit.
