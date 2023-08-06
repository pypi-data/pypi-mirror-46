sentry-regressions
==================

``sentry-regressions`` is a Sentry plugin that allows to better control
regression handling with non-linear backport releases.

In particular, this plugin considers the release versions when determining
whether an event is a regression or not, whereas stock Sentry does not. This
is of particular relevance if you're dealing with backport releases, where
a bugfix gets backported to a *lower* release that is more *recent* than the
one the issue was tagged as to be resolved in.

Consider this example:

- You release ``8.0``
- You find a trivial bug, and fix it in ``master``
- You release ``8.1``, containing that fix
- You resolve the Sentry issue as "resolved in 8.1"
- Now you backport a *different*, crucial fix from ``master`` back to an ``8.0.x`` LTS branch
- You release ``8.0.1``, which contains the crucial fix, but not the trivial one

So in chronological order you created the following releases:

- ``8.0``
- ``8.1``
- ``8.0.1``

If the trivial bug now occurs again in ``8.0.1``, stock Sentry will incorrectly
flag it as a regression, and reopen the issue. It's not a regression however,
because the trivial bug was never *supposed* to be fixed in ``8.0.1``, only
in ``8.1``. But because stock Sentry stricly goes by chronological release
dates, it considers the release ``8.0.1`` "higher" than ``8.1``.

This regression plugin will instead take actual **release versions** into
account when detecting regressions, by parsing version strings and comparing
them correctly (including natural sort order for numbers).

For parsing versions strings, the plugin will attempt to use the ``packaging``
module (via  `pkg_resources.parse_version() <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#parsing-utilities>`_)
if available to parse versions according to `Python's PEP440 <https://www.python.org/dev/peps/pep-0440/>`_.

While this is certainly suited for versions used in Python packages, the
version specification outlined in PEP 440 is pretty universal in its core,
and should be applicable to many other programming languages' versioning
conventions, unless you're using a very exotic versioning scheme.


Installation
============

Simply install the plugin via ``pip``:

.. code:: bash

    pip install sentry-regressions

The plugin then needs to be enabled on a per-project basis:

- Go to a Sentry project
- Settings
- Integrations -> All Integrations
- Enable the ``RegressionPlugin`` for the project

Compatibility
=============

Tested with:

- Sentry 9.1
- Sentry 8.22


Development
===========

- Create a virtualenv and activate it
- Create a  `Python Install of Sentry <https://docs.sentry.io/server/installation/python/>`_
- ``git clone https://github.com/4teamwork/sentry-regressions.git``
- ``cd sentry-regressions``
- ``pip install -e .``


Links
=====

- Github: https://github.com/4teamwork/sentry-regressions
- Issues: https://github.com/4teamwork/sentry-regressions/issues
- Pypi: http://pypi.python.org/pypi/sentry-regressions


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``sentry-regressions`` is licensed under GNU General Public License, version 2.
