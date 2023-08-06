setuptools-git-version
======================

*Automatically set package version from Git.*


Introduction
------------

Instead of hardcoding the package version in ``setup.py`` like:

.. code-block:: python

    setup(
        name='foobar',
        version='1.0',
        ...)

this package allows to extract it from the underlying Git repository:

.. code-block:: python

    setup(
        name='foobar',
        version_cc='{version}',
        setup_requires=['setuptools-git-version-cc'],
        ...)

Fields
------
``setuptools-git-version-cc`` provides a ``version`` number with this format:

..
    <major>.<minor>.<patch>-r<release>

where each component is computed using the Conventional Commits (CC). It is important 
to follow the structure of the commit message specified in the standard 
(see https://www.conventionalcommits.org/en/v1.0.0-beta.2/). The following fields
of the version are computed as follows

* ``major``: Incresed when the type of the commit is ``breaking`` (not ``BREAKING CHANGE`` as stated in the CC standard). This implies a breaking change in e.g. the interfaces. Numbering starts with 1.
* ``minor``: Incresed when the type of the commit is ``feat`` (new feature added to the code)
* ``patch``: Incresed when the type of the commit is ``fix`` (i.e. bugfix)
* ``release``: Increased when a type affects non production code (``chore``, ``ci``, ``test``...)

Implementation Details
----------------------

``setuptools-git-version`` uses the following git command to obtain commit information:

.. code-block:: bash

    git log --reverse --pretty=oneline

The script will parse all the messages and compute the version according to the
rules specified above

Deployment to PyPi
------------------

In order to deploy to PyPi

.. code-block:: bash

    # Install twine if you do not have it already
    pip install twine

    

More details on deployment can be found at https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives

    
