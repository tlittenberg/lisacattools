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

Report bugs at https://github.com/tlittenberg/lisacattools/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the Gitlab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the Gitlab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

lisacattools could always use more documentation, whether as part of the
official lisacattools docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/tlittenberg/lisacattools/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `{{ cookiecutter.project_slug }}` for local development.

1. Fork the lisacattools repo on Gitlab.
2. Clone your fork locally::

    $ git clone git@github.com:<your github id>/lisacattools.git

3. Install pyenv to test lisacattools with different versions of Python

    $ curl https://pyenv.run | bash
    $ echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    $ echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    $ source ~/.bashrc
    $ pyenv install 3.10 3.11 3.12

4. Install Poetry — Python's Packaging and Dependency Manager

    $ curl -sSL https://install.python-poetry.org | python3

5. Install your local copy into a virtualenv. Assuming you have virtualenv installed, this is how you set up your fork for local development::

    $ cd lisacattools
    $ make prepare-dev
    $ source .lisacattools
    $ make install-dev

6. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

7. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions with tox::

    $ make test
    $ make tox


8. Commit your changes and push your branch to Gitlab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the Github website.
