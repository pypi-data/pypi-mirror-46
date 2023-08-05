.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.ethz.ch/hvl_priv/hvl_ccb/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitLab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitLab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

HVL Common Code Base could always use more documentation, whether as part of the
official HVL Common Code Base docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.ethz.ch/hvl_priv/hvl_ccb/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `hvl_ccb` for local development.

1. Clone `hvl_ccb` repo from GitLab.

    $ git clone git@gitlab.ethz.ch:your_name_here/hvl_ccb.git

2. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv hvl_ccb
    $ cd hvl_ccb/
    $ python setup.py develop
    $ pip install -r requirements_dev.txt

3. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 hvl_ccb tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.
   You can also use the provided make-like shell script to run flake8 and tests::

   $ ./make.sh lint
   $ ./make.sh test

5. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a merge request through the GitLab website.

Merge Request Guidelines
------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The merge request should work for Python 3.7. Check
   https://gitlab.ethz.ch/hvl_priv/hvl_ccb/merge_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

* To run tests from a single file::

  $ py.test tests/test_hvl_ccb.py

  or a single test function::

  $ py.test tests/test_hvl_ccb.py::test_command_line_interface

* To add dependency, edit appropriate ``*requirements`` variable in the
  ``setup.py`` file and re-run::

  $ python setup.py develop

* To generate a PDF version of the Sphinx documentation instead of HTML use::

  $ rm -rf docs/hvl_ccb.rst docs/modules.rst docs/_build && sphinx-apidoc -o docs/ hvl_ccb && python -msphinx -M latexpdf docs/ docs/_build

  This command can also be run through the make-like shell script::

  $ ./make.sh docs-pdf

  This requires a local installation of a LaTeX distribution, e.g. MikTeX.

Deploying
---------

A reminder for the maintainers on how to deploy. Create release-N.M.K branch.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

  $ bumpversion patch # possible: major / minor / patch
  $ git push
  $ git push --tags
  $ make release

Merge the release branch into master and devel branches with :code:`--no-ff` flag.

Optionally, go to
https://gitlab.ethz.ch/hvl_priv/hvl_ccb/tags/vM.N.P/release/edit and add release
notes (e.g. changes lists).
