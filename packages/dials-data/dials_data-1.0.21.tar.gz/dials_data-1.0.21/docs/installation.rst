.. highlight:: shell

======================
Installation and Usage
======================

There are a number of possible ways to install ``dials_data``.
From the simplest to the most involved these are:


As an end user
^^^^^^^^^^^^^^

Quite simply: You do not need to install ``dials_data``.
It does not add any functionality to end users.


As a developer to run tests with ``dials_data``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may want to install ``dials_data`` so that you can run regression tests locally.
Or you might say that continuous integration should take care of this.
Both are valid opinions.

.. _basic-installation:

However you do not need to install ``dials_data`` from source. You can simply run::

    pip install -U dials_data

or, in a cctbx/DIALS environment::

    libtbx.pip install -U dials_data

This will install or update an existing installation of ``dials_data``.

In a cctbx/DIALS environment you may have to do a round of
``libtbx.configure`` or ``make reconf`` to enable the ``dials_data``
command line utilities.
In a normal Python environment this is not required.

You can then run your tests as usual using::

    pytest

although, depending on the configuration of the code under test, you
probably need to run it as::

    pytest --regression

to actually enable those tests depending on files from ``dials_data``.


As a developer to write tests with ``dials_data``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install ``dials_data`` using ``pip`` as above.

If your test is written in pytest and you use the fixture provided by
``dials_data`` then you can use regression datasets in your test by
adding the ``dials_data`` fixture to your test, ie:

.. code-block:: python

    def test_accessing_a_dataset(dials_data):
        location = dials_data("x4wide")

The fixture/variable ``dials_data`` in the test is a
``dials_data.download.DataFetcher`` instance, which can be called with
the name of the dataset you want to access (here: ``x4wide``). If the
files are not present on the machine then they will be downloaded.
If either the download fails or ``--regression`` is not specified then
the test is skipped.

The return value (``location``) is a ``py.path.local`` object pointing
to the directory containing the requested dataset.

You can see a list of all available datasets by running::

    dials.data list

or by going through the
`dataset definition files in the repository <https://github.com/dials/data/tree/master/dials_data/definitions>`__.

For a new project you may have to set up the ``dials_data`` fixture
first.
Assuming you are using ``pytest`` then simply add the following to a
file named ``conftest.py`` in the top level of your project:

.. code-block:: python

    import pytest
    try:
        from dials_data import *
    except ImportError:
        @pytest.fixture
        def dials_data():
            pytest.skip("Test requires python package dials_data")


As a developer who wants to add files to ``dials_data``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow the steps in :doc:`/contributing` to install ``dials_data`` into a
virtual environment.

You can install ``dials_data`` using ``pip`` as above *unless* you want to
immediately use your dataset definition in tests without waiting for your
pull request to be accepted. In this case you can follow the instructions
in the next step.


As a developer who wants to extend ``dials_data``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Have a look at the :doc:`/contributing` page.

Install your own fork of ``dials_data`` by running::

    pip install -e path/to/fork

in a cctbx/DIALS environment use ``libtbx.pip`` respectively, followed by
a round of ``libtbx.configure`` or ``make reconf``.

If you made substantial changes or updated your source copy you may also
have to run::

    python setup.py develop

or in a cctbx/DIALS environment::

    libtbx.python setup.py develop

followed by a round of ``libtbx.configure`` or ``make reconf``.
This will update your python package index and install/update any
``dials_data`` dependencies if necessary.

To switch back from using your checked out version to the 'official'
version of ``dials_data`` you can uninstall it with::

    pip uninstall dials_data # or
    libtbx.pip uninstall dials_data

and then reinstall it following the
`instructions at the top of this page <basic-installation_>`__.


Where are the regression datasets stored?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order of evaluation:

* If the environment variable ``DIALS_DATA`` is set and exists or can be
  created then use that location.
* If the file path ``/dls/science/groups/scisoft/DIALS/dials_data`` exists and is readable then
  use this location. This is a shared directory specific to Diamond Light Source.
* If the environment variable ``LIBTBX_BUILD`` is set and the directory
  ``dials_data`` exists or can be created underneath that location then
  use that.
* Use ``~/.cache/dials_data`` if it exists or can be created.
* Otherwise ``dials_data`` will fail with a RuntimeError.
