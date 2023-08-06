logwrap
=======

.. image:: https://travis-ci.com/python-useful-helpers/logwrap.svg?branch=master
    :target: https://travis-ci.com/python-useful-helpers/logwrap
.. image:: https://coveralls.io/repos/github/python-useful-helpers/logwrap/badge.svg?branch=master
    :target: https://coveralls.io/github/python-useful-helpers/logwrap?branch=master
.. image:: https://readthedocs.org/projects/logwrap/badge/?version=latest
    :target: http://logwrap.readthedocs.io/
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/logwrap.svg
    :target: https://pypi.python.org/pypi/logwrap
.. image:: https://img.shields.io/pypi/pyversions/logwrap.svg
    :target: https://pypi.python.org/pypi/logwrap
.. image:: https://img.shields.io/pypi/status/logwrap.svg
    :target: https://pypi.python.org/pypi/logwrap
.. image:: https://img.shields.io/github/license/python-useful-helpers/logwrap.svg
    :target: https://raw.githubusercontent.com/python-useful-helpers/logwrap/master/LICENSE


logwrap is a helper for logging in human-readable format function arguments and call result on function call.
Why? Because logging of `*args, **kwargs` become useless with project grow and you need more details in call log.

Cons:

* Log records are not single line.

Pros:

* Log records are not single 100500 symbols length line.
  (Especially actual for testing/development environments and for Kibana users).
* Service free: job is done by this library and it's dependencies. It works at virtualenv
* Free software: Apache license
* Open Source: https://github.com/python-useful-helpers/logwrap
* PyPI packaged: https://pypi.python.org/pypi/logwrap
* Self-documented code: docstrings with types in comments
* Tested: see bages on top
* Support multiple Python versions:

::

    Python 2.7
    PyPy

.. note:: 3.4 is supported in versions 4.9.*, 3.5+ in versions > 5.0.0.

This package includes helpers:

* `logwrap` - main helper. The same is `LogWrap`.

* `LogWrap` - class with `logwrap` implementation. May be used directly.

* `pretty_repr`

* `pretty_str`

* `PrettyFormat`

Usage
=====

logwrap
-------
The main decorator. Could be used as not argumented (`@logwrap.logwrap`) and argumented (`@logwrap.logwrap()`).
Not argumented usage simple calls with default values for all positions.

.. note:: Argumens should be set via keywords only.

Argumented usage with arguments from signature:

.. code-block:: python

    @logwrap.logwrap(
        log=logging.getLogger(__name__),  # __name__ = 'logwrap'
        log_level=logging.DEBUG,
        exc_level=logging.ERROR,
        max_indent=20,  # forwarded to the pretty_repr
        spec=None,  # use target callable function for spec
        blacklisted_names=None,  # list argument names, which should be dropped from log
        blacklisted_exceptions=None,  # Exceptions to skip in log
        log_call_args=True,  # Log call arguments before call
        log_call_args_on_exc=True,  # Log call arguments if exception happens
        log_result_obj=True,  # Log result object
    )

Usage examples:

.. code-block:: python

    @logwrap.logwrap()
    def foo():
        pass

is equal to:

.. code-block:: python

    @logwrap.logwrap
    def foo():
        pass

Get decorator for use without parameters:

.. code-block:: python

    get_logs = logwrap.logwrap()  # set required parameters via arguments

    type(get_logs) == LogWrap  # All logic is implemented in LogWrap class starting from version 2.2.0

    @get_logs
    def foo():
        pass

Call example:

.. code-block:: python

   import logwrap

   @logwrap.logwrap
   def example_function1(
           arg1: str,
           arg2: str='arg2',
           *args,
           kwarg1: str,
           kwarg2: str='kwarg2',
           **kwargs
   ) -> tuple():
       return (arg1, arg2, args, kwarg1, kwarg2, kwargs)

   example_function1('arg1', kwarg1='kwarg1', kwarg3='kwarg3')

This code during execution will produce log records:

::

    Calling:
    'example_function1'(
        # POSITIONAL_OR_KEYWORD:
        'arg1'=u'''arg1''',  # type: <class 'str'>
        'arg2'=u'''arg2''',  # type: <class 'str'>
        # VAR_POSITIONAL:
        'args'=(),
        # KEYWORD_ONLY:
        'kwarg1'=u'''kwarg1''',  # type: <class 'str'>
        'kwarg2'=u'''kwarg2''',  # type: <class 'str'>
        # VAR_KEYWORD:
        'kwargs'=
            dict({
                'kwarg3': u'''kwarg3''',
            }),
    )
    Done: 'example_function1' with result:

     tuple((
        u'''arg1''',
        u'''arg2''',
        (),
        u'''kwarg1''',
        u'''kwarg2''',
         dict({
            'kwarg3': u'''kwarg3''',
         }),
     ))

Limitations:

* nested wrapping (`@logwrap @deco2 ...`) is not parsed under python 2.7: `functools.wraps` limitation. Please set `logwrap` as the first level decorator.

LogWrap
-------
Example construction and read from test:

.. code-block:: python

    log_call = logwrap.LogWrap()
    log_call.log_level == logging.DEBUG
    log_call.exc_level == logging.ERROR
    log_call.max_indent == 20
    log_call.blacklisted_names == []
    log_call.blacklisted_exceptions == []
    log_call.log_call_args == True
    log_call.log_call_args_on_exc == True
    log_call.log_result_obj == True

On object change, variable types is validated.

In special cases, when special processing required for parameters logging (hide or change parameters in log),
it can be done by override `pre_process_param` and `post_process_param`.

See API documentation for details.


pretty_repr
-----------
This is specified helper for making human-readable repr on complex objects.
Signature is self-documenting:

.. code-block:: python

    def pretty_repr(
        src,  # object for repr
        indent=0,  # start indent
        no_indent_start=False,  # do not indent the first level
        max_indent=20,  # maximum allowed indent level
        indent_step=4,  # step between indents
        py2_str=False,  # use bytes for python 2 __repr__ and __str__
    )

Limitation: Dict like objects is always marked inside `{}` for readability, even if it is `collections.OrderedDict` (standard repr as list of tuples).

pretty_str
----------
This is specified helper for making human-readable str on complex objects.
Signature is self-documenting:

.. code-block:: python

    def pretty_str(
        src,  # object for __str__
        indent=0,  # start indent
        no_indent_start=False,  # do not indent the first level
        max_indent=20,  # maximum allowed indent level
        indent_step=4,  # step between indents
        py2_str=False,  # use bytes for python 2 __repr__ and __str__
    )

Limitations:
    Dict like objects is always marked inside `{}` for readability, even if it is `collections.OrderedDict` (standard repr as list of tuples).

    Iterable types is not declared, only brackets is used.

    String and bytes looks the same (its __str__, not __repr__).

PrettyFormat
------------
PrettyFormat is the main formatting implementation class.
`pretty_repr` and `pretty_str` uses instances of subclasses `PrettyRepr` and `PrettyStr` from this class.
This class is mostly exposed for typing reasons.
Object signature:

.. code-block:: python

    def __init__(
        self,
        max_indent=20,  # maximum allowed indent level
        indent_step=4,  # step between indents
        py2_str=False,  # use bytes for python 2 __repr__ and __str__
    )

Callable object (`PrettyFormat` instance) signature:

.. code-block:: python

    def __call__(
        self,
        src,  # object for repr
        indent=0,  # start indent
        no_indent_start=False  # do not indent the first level
    )

Adopting your code
------------------
pretty_repr behavior could be overridden for your classes by implementing specific magic method:

.. code-block:: python

    def __pretty_repr__(
        self,
        parser  # PrettyFormat class instance,
        indent  # start indent,
        no_indent_start  # do not indent the first level
    ):
        return ...

This method will be executed instead of __repr__ on your object.

.. code-block:: python

    def __pretty_str__(
        self,
        parser  # PrettyFormat class instance,
        indent  # start indent,
        no_indent_start  # do not indent the first level
    ):
        return ...

This method will be executed instead of __str__ on your object.

Testing
=======
The main test mechanism for the package `logwrap` is using `tox`.
Available environments can be collected via `tox -l`

CI systems
==========
For code checking several CI systems is used in parallel:

1. `Travis CI: <https://travis-ci.com/python-useful-helpers/logwrap>`_ is used for checking: PEP8, pylint, bandit, installation possibility and unit tests. Also it's publishes coverage on coveralls.

2. `coveralls: <https://coveralls.io/github/python-useful-helpers/logwrap>`_ is used for coverage display.

CD system
=========
`Travis CI: <https://travis-ci.com/python-useful-helpers/logwrap>`_ is used for package delivery on PyPI.
