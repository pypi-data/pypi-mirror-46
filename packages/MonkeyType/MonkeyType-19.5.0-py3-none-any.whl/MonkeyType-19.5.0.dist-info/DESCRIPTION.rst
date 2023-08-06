MonkeyType
==========

MonkeyType collects runtime types of function arguments and return values, and
can automatically generate stub files or even add draft type annotations
directly to your Python code based on the types collected at runtime.

Example
-------

Say ``some/module.py`` originally contains::

  def add(a, b):
      return a + b

And ``myscript.py`` contains::

  from some.module import add

  add(1, 2)

Now we want to infer the type annotation of ``add`` in ``some/module.py`` by
running ``myscript.py`` with ``MonkeyType``. One way is to run::

  $ monkeytype run myscript.py

By default, this will dump call traces into a SQLite database in the file
``monkeytype.sqlite3`` in the current working directory. You can then use the
``monkeytype`` command to generate a stub file for a module, or apply the type
annotations directly to your code.

Running ``monkeytype stub some.module`` will output a stub::

  def add(a: int, b: int) -> int: ...

Running  ``monkeytype apply some.module`` will modify ``some/module.py`` to::

  def add(a: int, b: int) -> int:
      return a + b

This example demonstrates both the value and the limitations of
MonkeyType. With MonkeyType, it's very easy to add annotations that
reflect the concrete types you use at runtime, but those annotations may not
always match the full intended capability of the functions. For instance, ``add``
is capable of handling many more types than just integers. Similarly, MonkeyType
may generate a concrete ``List`` annotation where an abstract ``Sequence`` or
``Iterable`` would be more appropriate. MonkeyType's annotations are an
informative first draft, to be checked and corrected by a developer.

Motivation
----------

Readability and static analysis are the primary motivations for adding type
annotations to code. It's already common in many Python style guides to
document the argument and return types for a function in its docstring;
annotations are a standardized way to provide this documentation, which also
permits static analysis by a typechecker such as `mypy`_.

For more on the motivation and design of Python type annotations, see
:pep:`483` and :pep:`484`.

.. _mypy: http://mypy.readthedocs.io/en/latest/

Requirements
------------

MonkeyType requires Python 3.6+ and the `retype`_ library (for applying type
stubs to code files). It generates only Python 3 type annotations (no type
comments).

Installing
----------

Install MonkeyType with `pip`_::

  pip install MonkeyType

How MonkeyType works
--------------------

MonkeyType uses the `sys.setprofile`_ hook provided by Python to interpose on
function calls, function returns, and generator yields, and record the types of
arguments / return values / yield values.

It generates `stub files`_ based on that data, and can use `retype`_ to apply those
stub files directly to your code.

.. _pip: https://pip.pypa.io/en/stable/
.. _retype: https://pypi.python.org/pypi/retype
.. _sys.setprofile: https://docs.python.org/3/library/sys.html#sys.setprofile
.. _stub files: http://mypy.readthedocs.io/en/latest/basics.html#library-stubs-and-the-typeshed-repo

.. end-here

See `the full documentation`_ for details.

.. _the full documentation: http://monkeytype.readthedocs.io/en/latest/

Troubleshooting
---------------

Check if your issue is mentioned in `the frequently asked questions`_ list.

.. _the frequently asked questions: http://monkeytype.readthedocs.io/en/stable/faq.html

LICENSE
-------

MonkeyType is BSD licensed.


Changelog
=========

19.5.0
------

* Mark ``monkeytype`` package as typed per PEP 561. Thanks Vasily Zakharov for 
  the report.
* Add ``-v`` option; don't display individual traces that fail to decode unless
  it is given.

19.1.1
------

* Pass ``--incremental`` to retype when applying stubs, so it doesn't choke on
  partial stubs (which can result from e.g. failures to decode some traces).

19.1.0
------

* Add ``--omit-existing-annotations`` option, implied by ``apply``. Merge of
  #129. Fixes #11 and #81.

* Render ``...`` for all parameter defaults in stubs. Remove the
  ``--include-unparsable-defaults`` and ``--exclude-unparsable-defaults`` CLI
  options, as well as the ``include_unparsable_defaults()`` config method.
  Merge of #128, fixes #123.

* Render forward references (from existing annotations) correctly. Merge of #127.

* Rewrite `Generator[..., None, None]` to `Iterator[None]` by default. Merge of
  #110, fixes #4. Thanks iyanuashiri.


18.8.0
------

* Support Python 3.7. Merge of #107, fixes #78.

* Print useful error message when filename is passed to stub/apply. Merge of
  #88, fixes #65. Thanks rajathagasthya.

* Fix crash in ``list_modules`` when there are no traces. Merge of #106, fixes
  #90.  Thanks tyrinwu.

* Enable ``python -m monkeytype {run,stub,apply} ...``. Merge of #100, fixes
  #99. Thanks retornam.


18.5.1
------

* Add ``MONKEYTYPE_TRACE_MODULES`` env var for easier tracing of code in
  site-packages. Merge of #83, fixes #82. Thanks Bo Peng.

* Fix passing additional arguments to scripts run via ``monkeytype run``. Merge
  of #85. Thanks Danny Qiu.

* Fix handling of spaces in filenames passed to retype. Merge of #79, fixes
  #77.

* Never render NoneType in stubs, substitute None.  Merge of #75, fixes #5.
  Thanks John Arnold.


18.2.0
------

* Move filtering of `__main__` module into CallTraceStoreLogger instead of core
  tracing code, so it can be overridden by special use cases like IPython
  tracing. Merge of #72, fixes #68. Thanks Tony Fast.

* Generate stubs for modules where the module file is like module/__init__.py.
  Print retype stdout/stderr. Merge of #69, Fixes #66.
  Thanks John Arnold.


18.1.13
-------

* Improve error messages in case of "no traces found" and/or file path given
  instead of module name. Merge of #37, partial fix for #65. Thanks Aarni
  Koskela.

* Add ``monkeytype list_modules`` sub-command to list all modules present in
  trace db. Merge of #61, fixes #60. Thanks Alex Miasoiedov.

* Add ``--diff`` option to ``monkeytype stub``. Merge of #59, fixes #58.
  Thanks Tai-Lin!

* Add ``--ignore-existing-annotations`` option to ``monkeytype stub``. Merge of
  #55, fixes #15. Thanks Tai-Lin!


18.1.11
-------

* Fix crash in RewriteEmptyContainers rewriter if a parameter has only empty
  container types in traces (and more than one). Fixes #53.


18.1.10
-------

* Display retype errors when stub application fails. Merge of #52, fixes #49.

* Add ``--sample-count`` option to show the number of traces a given stub is
  based on. Merge of #50, fixes #7. Thanks Tai-Lin.

* Add ``monkeytype run -m`` for running a module as a script. Merge of
  #41. Thanks Simon Gomizelj.

* Add support for Django's ``cached_property`` decorator. Merge of #46, fixes
  #9. Thanks Christopher J Wang.

* Catch and log serialization exceptions instead of crashing. Fixes #38, merge
  of #39.

* Fix bug in default code filter when Python lib paths are symlinked. Merge of
  #40. Thanks Simon Gomizelj.

17.12.3
-------

* Rewrite imports from _io module to io. (#1, merge of #32). Thanks Radhans
  Jadhao.

* Add Config.cli_context() as a hook for custom CLI initialization and cleanup
  logic (#28; merge of #29). Thanks Rodney Folz.

17.12.2
-------

* Exclude "frozen importlib" functions in default code filter.

* Fix passing args to script run with ``monkeytype run`` (#18; merge of
  #21). Thanks Rodney Folz.

* Fix generated annotations for NewType types (#22; merge of #23). Thanks
  Rodney Folz.

17.12.1
-------

* Fix using MonkeyType outside a virtualenv (#16). Thanks Guido van Rossum for
  the report.

17.12.0
-------

* Initial public version.


