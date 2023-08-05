.. _issue board: https://gitlab.com/hectormartinez/taika/issues

Contributing to Taika
=====================

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Fix Bugs
~~~~~~~~

Look through the `issue board`_ for issues tagged as "type: bug".

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the `issue board`_ for issues tagged as "type: feature-request"or
"type: enhancement".

Write Documentation
~~~~~~~~~~~~~~~~~~~

Documentation is always welcome, whether as part of the official Taika docs, in docstrings,
or even on the web in blog posts, articles, and such. Don't be shy and contribute :-D

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at `issue board`_. Select the template
that fits your needs and submit it!

Get Started!
------------

Ready to contribute? Here's how to set up `taika` for local development.

1. Fork the `taika` repo on GitLab.
2. Clone your fork locally::

   $ git clone git@gitlab.com:your_name_here/taika.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed,
   this is how you set up your fork for local development::

   $ mkvirtualenv taika -p python3.6
   $ cd taika/
   $ python setup.py develop
   $ pip install -r requirements.txt
   $ pre-commit install

4. Create a branch for local development::

   $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, run tox::

   $ tox

6. Commit your changes and push your branch to GitLab::

   $ git add .
   $ git commit
   $ git push origin name-of-your-bugfix-or-feature

7. Submit a merge request through the GitLab website.

Merge Request Guidelines
------------------------

Before you submit a merge request, check that it meets these guidelines:

1. Tests musts be included.
2. Documentation (docstrings or pages) must be included.
3. Python 3.6 should be supported.
4. The code should be isort'ed and flake8'ed. Optionally pylint'ed.

After you submit a merge request, check regularly the merge request, as
Continuous Integration is run for each of your commits and should pass in order
to merge the request.

Tips and tricks with pytest
----------------------------

Run all the test environments.

$ tox

To run only one environment::

$ tox -e <testenv>

To run a test module::

$ pytest tests/test_module

To run a test function inside a module::

$ pytest tests/test_module.py::test_function


