# btrdb-admin-python

This repo contains a quick and dirty Python3 implementation of the BTRDB administrative API.  

**Note: At the moment only some of ACL related calls are available**

**Note: due to the quick/informal nature of this codebase, the tests ONLY include integration tests that expect to connect to a REAL btrdb server.  A dotenv file or ENV config is required to run the tests**

# Usage

First, obtain a connection to the database using a valid username and password that is able to use the admin API.  Then you can execute admin methods directly off of the object.

    from btrdb_admin import connect

    db = connect("brtrdb.example.net:4411", username="marmaduke", password="usiB6iUsRLyn")
    users = db.get_all_users()

# Documentation

The project documentation is written in reStructuredText and is built using Sphinx, which also includes the docstring documentation from the `btrdb-admin` Python package. For your convenience, the `Makefile` includes a target for building the documentation:

    $ make html

This will build the HTML documentation in `docs/build`, which can be viewed using `open docs/build/index.html`. Other formats (PDF, epub, etc) can be built using `docs/Makefile`. The documentation is automatically built when pushed to GitHub and hosted on [Read The Docs](https://btrdb.readthedocs.io/en/latest/).

Note that the documentation also requires Sphinx and other dependencies to successfully build: `pip install -r docs/requirements.txt`.

## Tests

This project includes a suite of automated tests based upon [pytest](https://docs.pytest.org/en/latest/).  For your convenience, a `Makefile` has been provided with a target for evaluating the test suite.  Use the following command to run the tests.

    $ make test

Aside from basic unit tests, the test suite is configured to use [pyflakes](https://github.com/PyCQA/pyflakes) for linting and style checking as well as [coverage](https://coverage.readthedocs.io) for measuring test coverage.

Note that the test suite has additional dependencies that must be installed for them to successfully run: `pip install -r tests/requirements.txt`.
