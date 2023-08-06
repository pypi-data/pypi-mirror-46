Changelog
=========


0.3.0
-----

* Functions ``from_dict`` renamed ``from_sequence_dict``, and ``to_dict`` 
  renamed ``to_sequence_dict``.
* Added tests for the functions ``from_sequence_dict`` and ``to_sequence_dict``.
* Installation now requires pandas >= 0.21.

Release date: 2019-05-19

`View commits <https://github.com/jmenglund/pandas-charm/compare/v0.2.0...v0.3.0>`_



0.2.0
-----

* Added functions ``from_dict`` and ``to_dict`` for casting from and to dictionaries.
* Updated commands for Travis-CI.
* Updates to ``README.rst``.
* Updates to ``release-checklist.rst``.

Release date: 2019-02-23

`View commits <https://github.com/jmenglund/pandas-charm/compare/v0.1.3...v0.2.0>`_


0.1.3
-----

* Fixed bug in function ``frame_as_categorical`` that caused an error when
  trying to change the dtype to "category".
* Fixed problems with reporting test coverage.
* Removed Travis-CI testing for Python 3.3 and 3.4.
* Added Travis-CI testing for Python 3.6.
* List of included categories are now ignored in matrix conversions involving
  categorical data.
* ``pytest-cov`` removed from ``requirements.txt``.
* Updates to ``setup.py``.
* Updates to ``README.rst``.
* Updates to ``release-checklist.rst``.

Release date: 2017-08-25

`View commits <https://github.com/jmenglund/pandas-charm/compare/v0.1.2...v0.1.3>`_


0.1.2
-----

* Added Python versions for Travis-CI (3.3, 3.5)
* Added PEP8 check to Travis-CI
* Updates to ``README.rst``
    - Fixed issue with one example not working (``pc.to_charmatrix()``)
    - Updated text in various places
* Updates to ``release-checklist.rst``

Release date: 2016-08-08

`View commits <https://github.com/jmenglund/pandas-charm/compare/v0.1.1...v0.1.2>`_


0.1.1
-----

* Simplified builds with Travis-CI.
* DOI badge added to the top of ``README.rst``.
* Information on how to cite pandas-charm added to ``README.rst``.

Release date: 2016-07-05

`View commits <https://github.com/jmenglund/pandas-charm/compare/v0.1.0...v0.1.1>`_


0.1.0
-----

Initial release.

Includes the following functions:

* ``frame_as_categorical()``
* ``frame_as_object()``
* ``from_bioalignment()``
* ``from_charmatrix()``
* ``to_bioalignment()``
* ``to_charmatrix()``

Release date: 2016-07-05
