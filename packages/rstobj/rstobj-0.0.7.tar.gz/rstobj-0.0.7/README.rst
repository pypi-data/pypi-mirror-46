.. image:: https://readthedocs.org/projects/rstobj/badge/?version=latest
    :target: https://rstobj.readthedocs.io/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/rstobj-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/rstobj-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/rstobj-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/rstobj-project

.. image:: https://img.shields.io/pypi/v/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/pypi/l/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/pypi/pyversions/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/pypi/dm/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/rstobj-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://rstobj.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://rstobj.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://rstobj.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/rstobj-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/rstobj-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/rstobj-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/rstobj#files


Welcome to ``rstobj`` Documentation
==============================================================================

``rstobj`` is a library that construct Restructured Text markup or directives from Python Code. ``rstobj`` is based on ``jinja2``.

**The idea behind rstobj**:

RestructuredText is super powerful, way more powerful than markdown. But have you ever think of **customize YOUR OWN markup or directive and do some magic?**

`Sphinx Doc <http://www.sphinx-doc.org/en/master/>`_ is the ultimate doc build tool. With ``rstobj``, you can **easily create your own markup / directive, and hide complex workflow behind a single markup / directive**, then use it when you need it. Here's some ideas:

1. Use ``.. include-all-image::`` to automatically scan image file under a directory, create ``.. image::`` directive and organize everything in a table.
2. Separate comment and value of the config file, automatically create an document for a config file.
3. ...

I have a `Blog Post <https://github.com/MacHu-GWU/Tech-Blog/issues/6>`_ to share how to create a sphinx doc extension in 50 lines and customize your own directive (Sorry, its written in Chinese).


**Example**:

.. code-block:: python

    import rstobj # or from rstobj import *

    header = rstobj.markup.Header(title="Section1", header_level=1, auto_label=True)
    rst_header = header.render()
    print(rst_header)

    ltable = rstobj.directives.ListTable(
        data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
        title="Users",
        header=True,
    )
    rst = ltable.render()
    print(rst_ltable)

Output::

    .. _section1:

    Section1
    ========

    .. list-table:: Users
        :header-rows: 1
        :stub-columns: 0

        * - id
          - name
        * - 1
          - Alice
        * - 2
          - Bob

I recommend to use this in your jinja2 template, content of ``outut.rst``::

    {{ header.render() }}
    {{ ltable.render() }}

And use ``rstobj`` with ``sphinx-jinja`` library https://pypi.org/project/sphinx-jinja/ in sphinx doc project.

**Supported directives**:

- ``.. image::``
- ``.. list-table::``
- ``.. contents::``
- ``.. code-block::``
- ``.. include::``

**Supported markup**:

- ``Header``::

    .. _ref-label:

    Title
    =====

- ``URL``: ```Text <Target>`_``
- ``Reference``: ``:ref:`Text <Target>```


**If you need more features, please submit an issue to** https://github.com/MacHu-GWU/rstobj-project/issues


.. _install:

Install
------------------------------------------------------------------------------

``rstobj`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install rstobj

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade rstobj