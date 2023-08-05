History
=======

:tag:`v0.5.2` (YYYY-MM-DD)
--------------------------

Fixed
~~~~~

* ``taika.ext.rst`` was printing ``suffixes``.
* Now documents have `url` which is used to specify the path in the dest directory.
* Modified the extensions for the new document key `url`.
* rST include directory now works as it should.

Added
~~~~~

* ``collections`` extension that groups documents per pattern.
* ``excerpt`` extension added.
* ``rst`` extension now reads options from config file.


:tag:`v0.5.1` (2018-04-16)
--------------------------

Changed
~~~~~~~

* The metadata was saying that the package was compatible with versions of Python
  and was wrong. Tags, classifiers and requires added.
* Files are read as bytes, so all the plugins and tests were adapted.

:tag:`v0.5.0` (2018-04-16)
--------------------------

Added
~~~~~

* Extensions system.
* Two extensions: ``rst`` and ``layouts``.
* INI file configuration.
* Main ``Taika`` class to orchestrate managers and configuration.
* ``taika.ext.rst`` now exits on warnings.

Changed
~~~~~~~

* CLI parsing now is done by ``argparse``.

Fixed
~~~~~

* Documentation.


:tag:`v0.4.0` (2018-03-17)
---------------------------

Added
~~~~~

* CLI entry point via ``taika``.
* GitLab folder for issues and merge requests customization.
* Spell checker for the documentation.

Removed
~~~~~~~

* Certain folders that should be untracked.
* Unused badges on the README.


:tag:`v0.3.0` (2018-03-15)
--------------------------

Necessary BUMP to wrap my head around the schema.


:tag:`v0.2.1` (2018-03-15)
--------------------------

Added
~~~~~

* GitLab Continuous Integration.
* Configuration for pytest: now the working directory is the ``tests`` folder.

Removed
~~~~~~~

* Travis Continuous Integration.


:tag:`v0.2.0` (2018-03-15)
--------------------------

Added
~~~~~

* Added the skeleton for the project.
* Added the first functions and functionality via API.


0.1.X (YYYY-MM-DD)
------------------

This versions correspond to older taika versions that I've uploaded to PyPi.
