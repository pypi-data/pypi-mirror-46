
Basic Sums package
======================

``basicsusms`` is a package for computing structural sums and the effective conductivity of random composites.

Structural sums (also known as basic sums) are mathematical objects originating from the computational materials science, considered to form a set of geometric features of data represented by points or disks on the plane.

See the structural sums overview, package description, tutorials, example usage and API reference on http://basicsums.bitbucket.io

|

Documentation
-------------

The documentation for ``basicsusms`` is hosted on `Bitbucket
<http://basicsums.bitbucket.io>`_.

|

Requirements
------------

``basicsusms`` runs under Python 3 and is written in pure Python. The package requires following scientific packages: ``numpy``, ``matplotlib``, and ``sympy``.

A basic familiarity with Python is required.

|
    
Installation
------------

Releases are hosted on PyPI, hence the easiest way to get ``basicsusms`` is to install it with pip:

.. code-block:: bash

    pip install basicsums


You can also download the `repository
<https://bitbucket.org/basicsums/basicsums/downloads/>`_.

Once installed the package can be tested by running:

.. code-block:: bash

    from basicsums.tests import test
    test.run()

Function ``test.run()`` executes all doctests included in package's docstrings as well as in test files residing in the ``tests`` submodule.


|

License
-------

Copyright (c) 2017-2019, Wojciech Nawalaniec

``basicsusms`` is an open source software made available under the New BSD License. For details see the `LICENSE
<https://bitbucket.org/basicsums/basicsums/src/master/LICENSE.txt>`_. file.

