CHANGELOG
=========
Version 3.3.1
-------------
* Python 3.7 support validated

Version 3.3.0
-------------
* Type hints and stubs
* PEP0518
* Deprecation of `*args` for logwrap
* Fix empty `*args` and `**kwargs`
* allow override for arguments repr processing (pre- and post-processing)

Version 3.2.0
-------------
* Return logwrap function back with 2 branches: with arguments and not due to
  instances of classes are not converted to methods during class compilation.

Unit tests for found issue created.

Version 3.1.0
-------------
* Drop logwrap function. Use class as-is. `logwrap = LogWrap` (No API changes).

Version 3.0.2
-------------
* Fix package README.

Version 3.0.1
-------------
* Fix documents.
* Drop useless arguments.

Version 3.0.0
-------------
* Drop formatters.

Less magic (dict of methods).

.. warning:: ``PrettyFormat`` API changed: formatters are set in subclasses.

Version 2.7.3
-------------
Return cythonize. Error reason failed, crashing code will not be compiled.

Version 2.7.2
-------------
Urgent fix: cythonized code crashes on processing async code.

Version 2.7.0
-------------
* Python 3.3 support is ended. EOL is coming, test was run rarely.
* Move data from setup.cfg to __init__.py and setup.py

Version 2.6.2
-------------
Fix no __init__ in wheel.

Version 2.6.1
-------------
Python 2.7 compile failed -> exclude compile.

Version 2.6.0
-------------
* Cytonize, if possible.

Version 2.5.1
-------------
Base class for decorator has been extracted.
Requirements is extracted to requirements.txt
Update setup.py from doctedsted get_simple_vars_from_src.

Version 2.5.0
-------------
* Typing is required for all python versions due to:
  June 15, 2018: Python 3.7.0 final release, the typing module is no longer provisional
* Use slots due to usage of multiple instances per project


Version 2.4.2
-------------
* Use `ast.literal_eval` instead of `eval` in isolated env for `__init__.py` parsing.
* Do not rely on `six` in `setup.py`.

Version 2.4.1
-------------
* Support `frozenset` expansion.
* Use ast for version extraction and do not use danger of if's in `__init__.py` - installed without dependencies package should crash on import.

Version 2.4.0
-------------
* PyPy3 correct support and python 3.3 external asyncio.
* Move the most metadata from `setup.py` to `setup.cfg`.
* Drop deprecated code.

Version 2.3.5
-------------
* Allow to run setup.py on not installed package (`__init__.py` imports fix).
* Simplify code

Version 2.3.4
-------------
* Revert setup from PEP0508 to PEP0426 due to external tools support limitation

Version 2.3.3
-------------
* API docs rewritten by hand due to automatic generation limitations.

Version 2.3.2
-------------
* Setup was updated in conform to PEP0508

* AsyncLogWrap/async_logwrap deletion moved on v 2.4 as destructive action.

* Mark, that setup requires not pre-historic setuptools.

Version 2.3.0
-------------
* logwrap/LogWrap transparently supports coroutines on py3.4+. AsyncLogWrap/async_logwrap is deprecated and will be deleted in version 2.3.2.

Version 2.2.1
-------------
* Use six library for compatibility options (anyway, it's required by modern setuptools).

Version 2.2.0
-------------
* Async for python 3.4

* Object model

* Ignore list for exceptions

* Possibility to omit arguments log (call/exception/both)

* Possibility to omit result object log

Version 2.1.0
-------------
* Async version can run sync code (but anyway, decorator returns coroutine)

* Sync version produces warning on async code

Version 2.0.0
-------------
* Async version is added

* pep8 tests is moved to Python 3.6 due to `async_logwrap` syntax incompatibility with python < 3.5

Version 1.3.0
-------------
* Allowed to blacklist call arguments

Version 1.2.0
-------------
* Fix dict keys length calculation

* Simplify API

* Expand documentation

Version 1.1.1
-------------
* documentation fix

Version 1.1.0
-------------
* pretty_str has been implemented

Version 1.0.6
-------------
* Technical bump

Version 1.0.5
-------------
* Drop test-related code from package and setup.py

Version 1.0.4
-------------
* divide process and final result call

* allow override behavior per type by magic __pretty_{}__ method

* PrettyFormat class is public

Note: No major bump until ready:
    pretty_str implementation for usage in __str__ and print calls

Version 1.0.3
-------------
* Technical bump: was a false-negative ci results

Version 1.0.2
-------------
* Rework requirements: remove magic

* Start extending pretty_repr: object model

Version 1.0.1
-------------
* Circle CI was disabled: all has been moved to the Travis

* Covered several special cases by unit tests

* ReadTheDocs now working correctly

* Fixed legacy commentaries at docstring

Version 1.0.0
-------------
* Drop historical code and update documentation

Development was started with re-using of historic code,
but now it's clean package with minimal requirements
(funcsigs looks like copy-paste from inspect.signature + adoption to use on python 2.7
(Enum is not available, not using enum34 package)).

* Mark package as stable (tested by unit tests and external run).

Version 0.9.0
-------------
* get_arg_names and get_call_args now presents only for historical reasons

* logwrap now logs argument types as commentaries
(POSITIONAL_ONLY (builtins only) | POSITIONAL_OR_KEYWORD (standard) | VAR_POSITIONAL (e.g. *args) | KEYWORD_ONLY (Python 3+ only) | VAR_KEYWORD (e.g. **kwargs))

Version 0.8.5
-------------
* Use funcsigs instead of manual reimplementation of inspect.signature & supplemental

* Implement parsing of functions and methods (log interfaces in additional to standard repr)

* internal modules was moved to protected scope

Version 0.8.0
-------------
* Drop six requirement

Version 0.7.3
-------------
* Documentation update only

Version 0.7.2
-------------
Internal bump for CI systems check

Version 0.7.1
-------------

* Tests is included in package

* Docstrings and misprints in documents fixed

* CI CD

Version 0.7
-----------
Functional changes:

* Fixed difference of repr empty set() between python versions: replace by string `set()`


CI and structure changes:

* Added CHANGELOG

* Use CirceCI for pylint and coverage upload (uploaded from python 2.7)

* LICENSE file has been replaced by template from GitHub due to parsing issues

Version 0.6
-----------
* Started stabilization: package structure, tests, CI

Prior to 0.6
------------
Preparing package, CI and fixing found issues.
