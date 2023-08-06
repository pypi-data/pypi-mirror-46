pandas-charm
============

|Build-Status| |Coverage-Status| |PyPI-Status| |License| |DOI-URI|

pandas-charm is a small Python package for getting character
matrices (alignments) into and out of `pandas <http://pandas.pydata.org>`_.
Use this library to make pandas interoperable with
`BioPython <http://biopython.org>`_ and `DendroPy <http://dendropy.org>`_.

Convert between the following objects:

* BioPython MultipleSeqAlignment <-> pandas DataFrame
* DendroPy CharacterMatrix <-> pandas DataFrame
* "Sequence dictionary" <-> pandas DataFrame

The code has been tested with Python 2.7, 3.5 and 3.6.

Source repository: `<https://github.com/jmenglund/pandas-charm>`_

------------------------------------------

.. contents:: Table of contents
   :backlinks: none
   :local:


Installation
------------

For most users, the easiest way is probably to install the latest version
hosted on `PyPI <https://pypi.org/>`_:

.. code-block::

    $ pip install pandas-charm

The project is hosted at https://github.com/jmenglund/pandas-charm and
can also be installed using git:

.. code-block::

    $ git clone https://github.com/jmenglund/pandas-charm.git
    $ cd pandas-charm
    $ python setup.py install


You may consider installing pandas-charm and its required Python packages
within a virtual environment in order to avoid cluttering your system's
Python path. See for example the environment management system
`conda <http://conda.pydata.org>`_ or the package
`virtualenv <https://virtualenv.pypa.io/en/latest/>`_.


Running the tests
-----------------

Testing is carried out with `pytest <https://docs.pytest.org/>`_:

.. code-block::

    $ pytest -v test_pandascharm.py

Test coverage can be calculated with `Coverage.py
<https://coverage.readthedocs.io/>`_ using the following commands:

.. code-block::

    $ coverage run -m pytest
    $ coverage report -m pandascharm.py

The code follow style conventions in `PEP8
<https://www.python.org/dev/peps/pep-0008/>`_, which can be checked
with `pycodestyle <http://pycodestyle.pycqa.org>`_:

.. code-block::

    $ pycodestyle pandascharm.py test_pandascharm.py setup.py


Usage
-----

The following examples show how to use pandas-charm. The examples are
written with Python 3 code, but pandas-charm should work also with
Python 2.7+. You need to install BioPython and/or DendroPy manually
before you start:

.. code-block::

    $ pip install biopython
    $ pip install dendropy


DendroPy CharacterMatrix to pandas DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> import dendropy
    >>> dna_string = '3 5\nt1  TCCAA\nt2  TGCAA\nt3  TG-AA\n'
    >>> print(dna_string)
    3 5
    t1  TCCAA
    t2  TGCAA
    t3  TG-AA

    >>> matrix = dendropy.DnaCharacterMatrix.get(
    ...     data=dna_string, schema='phylip')
    >>> df = pc.from_charmatrix(matrix)
    >>> df
      t1 t2 t3
    0  T  T  T
    1  C  G  G
    2  C  C  -
    3  A  A  A
    4  A  A  A

By default, characters are stored as rows and sequences as columns
in the DataFrame. If you want rows to hold sequences, just transpose
the matrix in pandas:

.. code-block:: pycon

    >>> df.transpose()
        0  1  2  3  4
    t1  T  C  C  A  A
    t2  T  G  C  A  A
    t3  T  G  -  A  A


pandas DataFrame to Dendropy CharacterMatrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> import dendropy
    >>> df = pd.DataFrame({
    ...     't1': ['T', 'C', 'C', 'A', 'A'],
    ...     't2': ['T', 'G', 'C', 'A', 'A'],
    ...     't3': ['T', 'G', '-', 'A', 'A']})
    >>> df
      t1 t2 t3
    0  T  T  T
    1  C  G  G
    2  C  C  -
    3  A  A  A
    4  A  A  A

    >>> matrix = pc.to_charmatrix(df, data_type='dna')
    >>> print(matrix.as_string('phylip'))
    3 5
    t1  TCCAA
    t2  TGCAA
    t3  TG-AA


BioPython MultipleSeqAlignment to pandas DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> from io import StringIO
    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> from Bio import AlignIO
    >>> dna_string = '3 5\nt1  TCCAA\nt2  TGCAA\nt3  TG-AA\n'
    >>> f = StringIO(dna_string)  # make the string a file-like object
    >>> alignment = AlignIO.read(f, 'phylip-relaxed')
    >>> print(alignment)
    SingleLetterAlphabet() alignment with 3 rows and 5 columns
    TCCAA t1
    TGCAA t2
    TG-AA t3
    >>> df = pc.from_bioalignment(alignment)
    >>> df
      t1 t2 t3
    0  T  T  T
    1  C  G  G
    2  C  C  -
    3  A  A  A
    4  A  A  A


pandas DataFrame to BioPython MultipleSeqAlignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> import Bio
    >>> df = pd.DataFrame({
    ...     't1': ['T', 'C', 'C', 'A', 'A'],
    ...     't2': ['T', 'G', 'C', 'A', 'A'],
    ...     't3': ['T', 'G', '-', 'A', 'A']})
    >>> df
      t1 t2 t3
    0  T  T  T
    1  C  G  G
    2  C  C  -
    3  A  A  A
    4  A  A  A

    >>> alignment = pc.to_bioalignment(df, alphabet='generic_dna')
    >>> print(alignment)
    SingleLetterAlphabet() alignment with 3 rows and 5 columns
    TCCAA t1
    TGCAA t2
    TG-AA t3


"Sequence dictionary" to pandas DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> d = {
    ...     't1': 'TCCAA',
    ...     't2': 'TGCAA',
    ...     't3': 'TG-AA'
    ... }
    >>> df = pc.from_sequence_dict(d)
    >>> df
      t1 t2 t3
    0  T  T  T
    1  C  G  G
    2  C  C  -
    3  A  A  A
    4  A  A  A


pandas DataFrame to "sequence dictionary"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import pandas as pd
    >>> import pandascharm as pc
    >>> df = pd.DataFrame({
    ...     't1': ['T', 'C', 'C', 'A', 'A'],
    ...     't2': ['T', 'G', 'C', 'A', 'A'],
    ...     't3': ['T', 'G', '-', 'A', 'A']})
    >>> pc.to_sequence_dict(df)
    {'t1': 'TCCAA', 't2': 'TGCAA', 't3': 'TG-AA'}


The name
--------

pandas-charm got its name from the pandas library plus an acronym for
CHARacter Matrix.


License
-------

pandas-charm is distributed under the `MIT license <https://opensource.org/licenses/MIT>`_.


Citing
------

If you use results produced with this package in a scientific
publication, please just mention the package name in the text and
cite the Zenodo DOI of this project:

|DOI-URI|

Choose your preferred citation style in the "Cite as" section on the Zenodo
page.


Author
------

Markus Englund, `orcid.org/0000-0003-1688-7112 <http://orcid.org/0000-0003-1688-7112>`_


.. |Build-Status| image:: https://travis-ci.org/jmenglund/pandas-charm.svg?branch=master
   :target: https://travis-ci.org/jmenglund/pandas-charm
   :alt: Build status
.. |Coverage-Status| image:: https://codecov.io/gh/jmenglund/pandas-charm/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jmenglund/pandas-charm
   :alt: Coverage status
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/pandas-charm.svg
   :target: https://pypi.python.org/pypi/pandas-charm
   :alt: PyPI status
.. |License| image:: https://img.shields.io/pypi/l/pandas-charm.svg
   :target: https://raw.githubusercontent.com/jmenglund/pandas-charm/master/LICENSE.txt
   :alt: License
.. |DOI-URI| image:: https://zenodo.org/badge/62513333.svg
   :target: https://zenodo.org/badge/latestdoi/62513333
   :alt: DOI
