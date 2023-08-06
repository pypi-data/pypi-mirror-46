FUNPACK changelog
=================


1.1.0 (Tuesday 14th May 2019)
-----------------------------


Changed
^^^^^^^


* The ``--visit``/``-vi`` command line option will no longer be applied to
  variables which do not have an `instancing
  <https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi?id=9>`_ code 2.
  This is implemented in the :func:`.keepVisits` function.
* The :func:`.remove` and :func:`.keepVisits` function signatures have changed
  - they now require the variable table to be passed in as the first argument.


1.0.2 (Tuesday 14th May 2019)
-----------------------------


Changed
^^^^^^^


* The :func:`.removeIfSparse` processing function accepts an ``ignoreType``
  parameter which forces all tests to be run, regardless of the variable type.


Fixed
^^^^^


* The :func:`.isSparse` function was skipping the ``mincat``/``maxcat`` tests
  for non-numeric categorical variables.


1.0.1 (Friday 9th May 2019)
---------------------------


Changed
^^^^^^^


* Python package name changed from ``fmrib_unpack`` to ``fmrib-unpack``.


1.0.0 (Friday 9th May 2019)
---------------------------


Changed
^^^^^^^


* ``ukbparse`` is now called ``FUNPACK`` - the *FMRIB UKBiobank Normalisation,
  Processing And Cleaning Kit*.


Removed
^^^^^^^


* The ``ukbparse_htmlparse``, ``ukbparse_join``, and
  ``ukbparse_compare_tables`` scripts have been removed.
* The ``ukbparse.icd10.readICD10CodingFile`` function and
  ``ukbparse.icd10.ICD10Hierarchy`` class have been removed (their
  functionality was replaced by the :mod:`.hierarchy` module)
* The :func:`.processing_functions.removeIfSparse` and
  :func:`.processing_functions_core.removeIfSparse` functions no longer accept
  an ``absolute`` argument.



0.21.1 (Thursday 8th May 2019)
------------------------------


Changed
^^^^^^^


* Addd categories 1, 2 and 99 to the ``fmrib`` configuration.



0.21.0 (Thursday 8th May 2019)
------------------------------


Added
^^^^^


* :class:`.Column` objects now have a ``metadata`` attribute which may be used
  in the column description (if the ``--description_file`` option is used).
  Processing functions can set the metadata for newly added columns.
* New ``metaproc`` plugin type to manipulate column metadata.
* All processing functions accept a ``metaproc`` argument, allowing a
  ``metaproc`` function to be applied to any column metadata that is returned
  by the processing function..


Changed
^^^^^^^


* The :func:`.binariseCategorical` function sets the categorical value as
  column metadata on the new binarised columns.


0.20.1 (Wednesday 8th May 2019)
-------------------------------


Fixed
^^^^^


* Fixed some typos in the ``README`` file.


0.20.0 (Tuesday 7th May 2019)
-----------------------------


Added
^^^^^


* The :func:`.isSparse` and :func:`.removeIfSparse` functions accept
  a new option, ``mincat``, which allows a categorical to be deemed sparse
  if the size of its smallest category is below a given threshold.
* New ``--description_file`` option which, for UK BioBank data, saves the
  description for each column to a text file.


Changed
^^^^^^^


* The ``absolute`` parameter to the :func:`.isSparse` and
  :func:`.removeIfSparse` functions is deprecated. Instead, they now accept
  ``abspres`` and ``abscat`` arguments, allowing the
  absoluteness/proportionality of the ``minpres`` and ``mincat``/``maxcat``
  options to be specified separately.
* Changed default processing rules so that ICD10 variables undergo a slightly
  different sparsity test.


Fixed
^^^^^


* Fixed a bug in the categorical recoding rules for Data Coding `100012
  <https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=100012>`_.



0.19.2 (Friday 26th April 2019)
-------------------------------


Changed
^^^^^^^


* Changes to built-in categories and to ``fmrib`` configuration.


0.19.1 (Thursday 25th April 2019)
---------------------------------


Changed
^^^^^^^


* Changed the default processing rules for ICD10 variables 40001, 40002,
  40006, 41202, and 41204.
* Added ICD10 variables 41201 and 41270 to the default cleaning/processing
  rules.


0.19.0 (Wednesday 24th April 2019)
----------------------------------


Added
^^^^^


* The ``--column`` option now accepts a file which contains a list of column
  names to import.


Changed
^^^^^^^


* The :func:`.icd10.codeToNumeric` and :func:`.icd10.numericToCode` functions
  have been changed to use the integer node IDs in the ICD10 hierarchy
  file. The previous approach could not handle parent categories, nor a small
  number of ICD10 codes which do not have a ``<letter><number>`` structure.
* The :func:`.fileinfo.has_header` function has been made more lenient for
  files with a small number of columns.


0.18.0 (Tuesday 23rd April 2019)
--------------------------------


Added
^^^^^


* New :func:`.icd10.numericToCode` function for converting from a numeric
  ICD10 code representation back to its alphanumeric representation.


Changed
^^^^^^^


* The default binarised ICD10 column name format has been changed from
  ``[variable_id][numeric_code]-[visit].0`` to
  ``[variable_id]-[visit].[numeric_code]``.
* The ``--non_numeric_file`` will not be created if there are not any
  non-numeric columns.
* The built-in ``fmrib`` configuration now includes verbosity and logging
  settings.
* The :func:`.isSparse` function now returns the reason and value for
  columns which fail the sparsity test.



0.17.0 (Monday 22nd April 2019)
-------------------------------


Added
^^^^^


* New ``--non_numeric_file`` option allows non-numeric columns to be saved to
  a separate file (TSV export only).
* Built-in ``fmrib.cfg`` configuration file, which can be used via
  ``-cfg fmrib``.


Changed
^^^^^^^


* The file generated by ``--unknown_vars_file`` now includes variables which
  are known, but are not in an existing category, and do not have any cleaning
  or processing rules specified for them.
* Built-in categories have been updated.


Fixed
^^^^^


* A bug in the column names generated for binarised ICD10 categorical codes
  has been fixed. This bug would potentially have resulted in collisions
  between column names for different ICD10 codes.


0.16.0 (Friday 22nd March 2019)
-------------------------------


Changed
^^^^^^^


* Full variable and datacoding table files no longer need to be provided -
  ``ukbparse`` uses ``ukbparse/data/field.txt`` and
  ``ukbparse/data/encoding.txt`` files, obtained from the UK Biobank showcase
  website, as the basis for recognising variables and data codings. The
  ``--variable_file``/``-vf`` and ``--datacoding_file``/``-df`` options now
  accept partial table definitions - these will be merged with the built-in
  rules (still stored in ``ukbparse/data/variables_*.tsv`` and
  ``ukbparse/data/datacodings_*.tsv``) when ``ukbparse`` is invoked.


Deprecated
^^^^^^^^^^


* The ``ukbparse_htmlparse``, ``ukbparse_join`` , and
  ``ukbparse_compare_tables`` commands.


Removed
^^^^^^^


* The ``--icd10_file`` command-line option has been removed.


0.15.1 (Thursday 21st March 2019)
---------------------------------


Fixed
^^^^^


* Fixed a bug which arose when using the ``--rename_column`` option.


0.15.0 (Monday 18th March 2019)
-------------------------------


Added
^^^^^


* New cleaning function, :func:`.flattenHierarchical`, for use with
  hierarchical variables (e.g. ICD10). The function can be used to replace
  leaf values with parent values.
* New :mod:`.hierarchy` module which contains helper functions and data
  structures for working with hierarchical variables.
* Definitions for all hierarchical UK Biobank variables are located in the
  ``ukbparse/data/hierarchy/`` directory.


Deprecated
^^^^^^^^^^


* The :func:`.readICD10ConfigFile` function has been replaced with the
  :func:`.loadHierarchyFile` function.
* The :class:`.ICD10Hierarchy` class has been replaced with the
  :class:`.Hierarchy` class .


0.14.8 (Monday 18th March 2019)
-------------------------------


Fixed
^^^^^


* Fixed an issue with the :func:`.binariseCategorical` processing function
  being applied to ICD10 codes.


0.14.7 (Sunday 17th March 2019)
-------------------------------


Changed
^^^^^^^


* Changes to default cleaning rules - negative values for integer/categorical
  types are no longer discarded.


0.14.6 (Saturday 16th March 2019)
---------------------------------


Fixed
^^^^^


* Fixed a ``KeyError`` which was occurring during the child-value replacement
  stage for input files which did not have column names of the form
  ``[variable]-[visit].[instance]``.
* Fixed some issues introduced by behavioural changes in the
  ``pandas.HDFStore`` class.


0.14.5 (Thursday 17th January 2019)
-----------------------------------


Fixed
^^^^^


* Implemented a workaround for a `bug <https://bugs.python.org/issue9334>`_ in
  the Python ``argparse`` module.


0.14.4 (Friday 11th January 2019)
---------------------------------


Changed
^^^^^^^


* Updated the default processing rules for variable
  [1120-1150](https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=1120).


0.14.3 (Tuesday 8th January 2019)
---------------------------------


Fixed
^^^^^


* Fixed a regression introduced in 0.14.2, where column loading restrictions
  (e.g. ``--variable``) were not being honoured


0.14.2 (Monday 7th January 2019)
--------------------------------


Fixed
^^^^^


* Fixed a regression introduced in 0.14.1, where using the ``--variable`` and
  ``--visit`` options together could cause a crash.


0.14.1 (Monday 7th January 2019)
--------------------------------


Fixed
^^^^^


* If the index columns for each input file have different names, the output
  index column was unnamed.  It is now given the name of the index column in
  the first input file.
* When the ``--column`` and ``--variable`` options were used together, only
  columns which passed both tests were being loaded. Now, columns which pass
  either test are loaded.


0.14.0 (Tuesday 25th December 2018)
-----------------------------------


Added
^^^^^


* New ``--column`` option, allowing columns to be selected by name/name
  pattern.
* ``ukbparse`` can now be installed from `conda-forge
  <https://anaconda.org/conda-forge/ukbparse>`_.


Changed
^^^^^^^


* The index column in the output file no longer defaults to being named
  ``'eid'``. It defaults to the name of the index in the input file, but
  can still be overridden by the ``--output_id_column`` option.


Fixed
^^^^^


* Blank lines are now allowed in configuration files (#2)
* Fix to derived column names for ICD10 variables in default processing rules.


0.13.1 (Thursday 20th December 2018)
------------------------------------


Added
^^^^^


* Unit test to make sure that ``ukbparse`` crashes if given bad input
  arguments.


0.13.0 (Thursday 20th Deember 2018)
-----------------------------------


Added
^^^^^


* New ``--index`` option, allowing the position of the index column in input
  files to be specified.
* The ``--variable``, ``--subject``, and ``--exclude`` options now accept
  comma-separated lists, in addition to IDs, ID ranges, and text files.


Fixed
^^^^^


* Memory usage estimates in log messages were wrong under Linux.


0.12.3 (Tuesday 18th December 2018
----------------------------------


Changed
^^^^^^^


* Changes to new :func:`.fileinfo.has_header` function to improve robustness.


0.12.2 (Monday 17th December 2018)
----------------------------------


Changed
^^^^^^^


* Now using a custom implementation of ``csv.Sniffer.has_header``, as the
  standard library version does not handle some scenarios.


0.12.1 (Saturday 15th December 2018)
------------------------------------


Added
^^^^^


* Added some instructions for generating your own variable and data coding
  tables to the README.


Changed
^^^^^^^


* The ``ukbparse_demo`` script ensures that the Jupyter ``bash_kernel`` is
  installed.
* The ``ukbparse_compare_tables``, ``ukbparse_htmlparse`` and
  ``ukbparse_join`` scripts print some help documentation when called without
  any arguments.
* Added ``lxml`` as a dependency (required by ``beautifulsoup4``).


0.12.0 (Tuesday 11th December 2018)
-----------------------------------


Added
^^^^^


* The ``join``, ``compare_tables``, and ``htmlparse`` scripts are now
  installed as entry points called ``ukbparse_join``,
  ``ukbparse_compare_tables``, and ``ukbparse_htmlparse``.
* Jupyter notebook, demonstrating most of the features in ``ukbparse``, at
  ``ukbparse/demo/ukbparse_demonstration.ipynb``. You can run the demo via the
  ``ukbparse_demo`` entry point.


Changed
^^^^^^^


* Moved the ``scripts/`` directory into the ``ukbparse/`` directory.
* Improved string representation of process functions.


Fixed
^^^^^


* Fix to configuration file parsing code - ``shlex.split`` is now used instead
  of ``str.split``.
* Fixed mixed data type issues when merging the data coding and type tables into
  the variable table.


0.11.3 (Monday 10th December 2018)
----------------------------------


Changed
^^^^^^^


* Made the ``vid``, ``visit``, and ``instance`` parameters to the
  :class:`.Column` class optional, to make life easier for custom sniffer
  functions.


0.11.2 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the handling of new variable IDs returned by processing
  functions.



0.11.1 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the :func:`.removeIfSparse` processing function.


0.11.0 (Monday 10th December 2018)
----------------------------------


Added
^^^^^


* New ``--no_builtins`` option, which causes the built-in variable, data
  coding, type, and category table files to be bypassed.
* New :meth:`.PluginRegistry.get` function for getting a reference to a plugin
  function.
* Cleaning/processing functions are listed in command-line help.


0.10.5 (Saturday 8th December 2018)
-----------------------------------


Changed
^^^^^^^


* The ``minpres`` option to the :func:`.removeIfSparse` processing function
  is ignored if it is specified as an absolute value, and the data set length
  is less than it.


0.10.4 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Fixed an issue with the `--subject` command line option.


0.10.3 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Made use of the standard library ``resource`` module conditional, as it is
  not present on Windows.


0.10.2 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Removed relative imports from test modules.


0.10.1 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* The :mod:`ukbparse.plugins` package was missing an ``__init__.py``, and was
  not being included in PyPI packages.


0.10.0 (Thursday 6th December 2018)
-----------------------------------


Added
^^^^^


* New ``--na_values``, ``--recoding``, and ``--child_values`` command-line
  options for specifying/overriding NA insertion, categorical recodings,
  and child variable value replacement.
* ``--dry_run`` mode now prints information about columns that would not be
  loaded.


Fixed
^^^^^


* Fixed a bug in the :func:`.calculateExpressionEvaluationOrder` function.


0.9.0 (Thursday 6th December 2018)
----------------------------------


Added
^^^^^


* Infrastructure for automatic deployment to PyPI and Zenodo.


Changed
^^^^^^^


* Improved ``--dry_run`` output formatting.


0.8.0
-----


Added
^^^^^


* New ``--dry_run`` command-line option, which prints a summary of the cleaning
  and processing that would take place.


0.7.1
-----


Fixed
^^^^^


* Fixed a bug in the :func:`.icd10.saveCodes` function.


0.7.0
-----


Changed
^^^^^^^


* Small refactorings in :mod:`ukbparse.config` so that command line arguments
  can be logged easily.


0.6.3
-----


Changed
^^^^^^^


* Minor updates to avoid deprecation warnings.


0.6.2
-----


Fixed
^^^^^


* Fixed a bug with the ``--import_all`` option, where an error would be thrown
  if a specifically requested variable was removed during processing.


0.6.1
-----


Changed
^^^^^^^


* Changed default processing for variables 41202/41204 so they are binarised
  *within* visit.


0.6.0
-----


Added
^^^^^


* New ``--import_all`` and ``--unknown_vars_file`` options for outputting
  information about previously unknown variables/columns.


Changed
^^^^^^^


* Changed processing function return value interface - see the
  :mod:`.processing_functions` module for details.


0.5.0
-----


Added
^^^^^


* Ability to export a mapping file containing the numeric values that ICD10
  codes have been converted into - see the ``--icd10_map_file`` argument.


Changed
^^^^^^^


* Changes to default processing - all ICD10 variables are binarised by default.
  Sparsity/redundancy tests happen at the end, so that columns generated by
  previous steps are tested.


Fixed
^^^^^


* :meth:`.HDFStoreCollection.loc` method returns a ``pandas.DataFrame`` when
  a list of columns are indexed, and a ``pandas.Series`` when a single column
  is indexed.


0.4.1
-----


Changed
^^^^^^^


* Updates to variable table for UKBiobank spirometry variables.


0.4.0
-----


Added
^^^^^


* New :func:`.parseSpirometryData` function for parsing spirometry data
  (i.e. `UKBiobank variable 3066
  <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=3066>`_


Removed
^^^^^^^


* Removed the ``--disable_rename`` command line option, because having the
  columns renamed is really annoying.


0.3.3
-----


Changed
^^^^^^^


* Reverted the behaviour of :func:`.isSparse`.


0.3.2
-----


Changed
^^^^^^^


* Changed the behaviour of :func:`.isSparse` so that series which are *greater
  than* the ``minpres`` threshold pass, rather than *greater than or equal
  to*.


0.3.1
-----


Changed
^^^^^^^


* The :func:`.isSparse` function ignores the ``minpres`` argument if it
  is larger than the number of samples in the data set.


Fixed
^^^^^


* The :func:`.binariseCategorical` function now works on data with missing
  values.


0.3.0
-----


Added
^^^^^


* New :meth:`.DataTable.addColumns` method, so processing functions can
  now add new columns.
* New :func:`.binariseCategorical` processing function, which expands a
  categorical column into multiple binary columns, one for each unique
  value in the data.
* New :func:`.expandCompound` processing function, which expands a
  compound column into columns, one for each value in the compound data.
* Keyword arguments can now be used when specifying processing.


Fixed
^^^^^


* Fixed handling of non-numeric categorical variables


0.2.0
-----


Added
^^^^^

* Added a changelog file


Changed
^^^^^^^


* Updated variable/datacoding files to bring them in line with the latest
  Biobank data release.
