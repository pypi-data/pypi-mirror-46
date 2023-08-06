
DepHell Archive
===============


.. image:: https://travis-ci.org/dephell/dephell_archive.svg?branch=master
   :target: https://travis-ci.org/dephell/dephell_archive
   :alt: travis


.. image:: https://ci.appveyor.com/api/projects/status/github/dephell/dephell_archive?svg=true
   :target: https://ci.appveyor.com/project/orsinium/dephell-archive
   :alt: appveyor


.. image:: https://img.shields.io/pypi/l/dephell-archive.svg
   :target: https://github.com/dephell/dephell_archive/blob/master/LICENSE
   :alt: MIT License


Module to work with files and directories in archive in `pathlib <https://docs.python.org/3/library/pathlib.html>`_ style.


* **Goal:** provide the same interface as ``pathlib.Path`` for archives.
* **State:** partially implemented. Need to implement more methods.

Installation
------------

Install from `PyPI <https://pypi.org/project/dephell-archive/>`_\ :

.. code-block:: bash

   python3 -m pip install --user dephell_archive

Usage
-----

.. code-block:: python

   from pathlib import Path
   from tempfile import TemporaryDirectory

   from dephell_archive import ArchivePath

   with TemporaryDirectory() as cache:
     path = ArchivePath(
       archive_path=Path('tests', 'requirements', 'wheel.whl'),
       cache_path=Path(cache),
     )
     subpath = path / 'dephell' / '__init__.py'
     with subpath.open() as stream:
       content = stream.read()
