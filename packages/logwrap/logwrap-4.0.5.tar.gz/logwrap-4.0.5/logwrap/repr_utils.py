#    Copyright 2018 - 2019 Alexey Stepanov aka penguinolog

#    Copyright 2016 Mirantis, Inc.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""repr_utils module.

This is no reason to import this submodule directly, all required methods is
available from the main module.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

# Standard Library
import abc
import types
import typing  # noqa # pylint: disable=unused-import

# External Dependencies
import six

# LogWrap Implementation
# noinspection PyUnresolvedReferences
import funcsigs  # type: ignore

__all__ = ("PrettyFormat", "PrettyRepr", "PrettyStr", "pretty_repr", "pretty_str")


def _known_callable(item):  # type: (typing.Any) -> bool
    """Check for possibility to parse callable."""
    return isinstance(item, (types.FunctionType, types.MethodType))


def _simple(item):  # type: (typing.Any) -> bool
    """Check for nested iterations: True, if not."""
    return not isinstance(item, (list, set, tuple, dict, frozenset))


class ReprParameter(object):
    """Parameter wrapper wor repr and str operations over signature."""

    __slots__ = ("_value", "_parameter")

    POSITIONAL_ONLY = funcsigs.Parameter.POSITIONAL_ONLY
    POSITIONAL_OR_KEYWORD = funcsigs.Parameter.POSITIONAL_OR_KEYWORD
    VAR_POSITIONAL = funcsigs.Parameter.VAR_POSITIONAL
    KEYWORD_ONLY = funcsigs.Parameter.KEYWORD_ONLY
    VAR_KEYWORD = funcsigs.Parameter.VAR_KEYWORD

    empty = funcsigs.Parameter.empty

    def __init__(self, parameter, value=funcsigs.Parameter.empty):  # type: (funcsigs.Parameter, typing.Any) -> None
        """Parameter-like object store for repr and str tasks.

        :param parameter: parameter from signature
        :type parameter: inspect.Parameter
        :param value: default value override
        :type value: typing.Any
        """
        self._parameter = parameter
        self._value = value if value is not parameter.empty else parameter.default

    @property
    def parameter(self):  # type: () -> funcsigs.Parameter
        """Parameter object."""
        return self._parameter

    @property
    def name(self):  # type: () -> typing.Union[None, str]
        """Parameter name.

        For `*args` and `**kwargs` add prefixes
        """
        if self.kind == funcsigs.Parameter.VAR_POSITIONAL:
            return "*" + self.parameter.name  # type: ignore
        elif self.kind == funcsigs.Parameter.VAR_KEYWORD:
            return "**" + self.parameter.name  # type: ignore
        return self.parameter.name  # type: ignore

    @property
    def value(self):  # type: () -> typing.Any
        """Parameter value to log.

        If function is bound to class -> value is class instance else default value.
        """
        return self._value

    @property
    def annotation(self):  # type: () -> typing.Union[funcsigs.Parameter.empty, str]
        """Parameter annotation."""
        return self.parameter.annotation

    @property
    def kind(self):  # type: () -> int
        """Parameter kind."""
        return self.parameter.kind  # type: ignore

    def __hash__(self):  # type: () -> int  # pragma: no cover
        """Block hashing.

        :raises TypeError: Not hashable.
        """
        msg = "unhashable type: '{0}'".format(self.__class__.__name__)
        raise TypeError(msg)

    def __repr__(self):  # type: () -> str
        """Debug purposes."""
        return '<{} "{}">'.format(self.__class__.__name__, self)


# pylint: disable=no-member
def _prepare_repr(func):  # type: (typing.Union[types.FunctionType, types.MethodType]) -> typing.List[ReprParameter]
    """Get arguments lists with defaults.

    :param func: Callable object to process
    :type func: typing.Union[types.FunctionType, types.MethodType]
    :return: repr of callable parameter from signature
    :rtype: typing.List[ReprParameter]
    """
    ismethod = isinstance(func, types.MethodType)
    self_processed = False
    result = []
    if not ismethod:
        real_func = func
    else:
        real_func = func.__func__  # type: ignore

    for param in funcsigs.signature(real_func).parameters.values():
        if not self_processed and ismethod and func.__self__ is not None:  # type: ignore
            result.append(ReprParameter(param, value=func.__self__))  # type: ignore
            self_processed = True
        else:
            result.append(ReprParameter(param))

    return result


# pylint: enable=no-member


class PrettyFormat(object):
    """Pretty Formatter.

    Designed for usage as __repr__ and __str__ replacement on complex objects
    """

    __slots__ = ("__max_indent", "__indent_step", "__py2_str")

    def __init__(
        self,
        max_indent=20,  # type: int
        indent_step=4,  # type: int
        py2_str=False,  # type: bool
    ):  # type: (...) -> None
        """Pretty Formatter.

        :param max_indent: maximal indent before classic repr() call
        :type max_indent: int
        :param indent_step: step for the next indentation level
        :type indent_step: int
        :param py2_str: use Python 2.x compatible strings instead of unicode
        :type py2_str: bool
        """
        self.__max_indent = max_indent
        self.__indent_step = indent_step
        self.__py2_str = py2_str and not six.PY3  # Python 2 only behavior

    @property
    def max_indent(self):  # type: () -> int
        """Max indent getter.

        :rtype: int
        """
        return self.__max_indent

    @property
    def indent_step(self):  # type: () -> int
        """Indent step getter.

        :rtype: int
        """
        return self.__indent_step

    def next_indent(self, indent, multiplier=1):  # type: (int, int) -> int
        """Next indentation value.

        :param indent: current indentation value
        :type indent: int
        :param multiplier: step multiplier
        :type multiplier: int
        :return: next indentation value
        :rtype: int
        """
        return indent + multiplier * self.indent_step

    @abc.abstractmethod
    def _repr_callable(
        self, src, indent=0
    ):  # type: (typing.Union[types.FunctionType, types.MethodType], int) -> typing.Text
        """Repr callable object (function or method).

        :param src: Callable to process
        :type src: typing.Union[types.FunctionType, types.MethodType]
        :param indent: start indentation
        :type indent: int
        :return: Repr of function or method with signature.
        :rtype: typing.Text
        """
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def _repr_simple(self, src, indent=0, no_indent_start=False):  # type: (typing.Any, int, bool) -> typing.Text
        """Repr object without iteration.

        :param src: Source object
        :type src: typing.Any
        :param indent: start indentation
        :type indent: int
        :param no_indent_start: ignore indent
        :type no_indent_start: bool
        :return: simple repr() over object
        :rtype: typing.Text
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _repr_dict_items(
        self, src, indent=0
    ):  # type: (typing.Dict[typing.Any, typing.Any], int) -> typing.Iterator[typing.Text]
        """Repr dict items.

        :param src: object to process
        :type src: typing.Dict
        :param indent: start indentation
        :type indent: int
        :rtype: typing.Iterator[typing.Text]
        """
        raise NotImplementedError()

    @staticmethod
    def _repr_iterable_item(
        newline,  # type: bool
        obj_type,  # type: str
        prefix,  # type: str
        indent,  # type: int
        result,  # type: str
        suffix,  # type: str
    ):  # type: (...) -> typing.Text
        """Repr iterable item.

        :param newline: newline before item
        :type newline: bool
        :param obj_type: Object type
        :type obj_type: str
        :param prefix: prefix
        :type prefix: str
        :param indent: start indentation
        :type indent: int
        :param result: result of pre-formatting
        :type result: str
        :param suffix: suffix
        :type suffix: str
        :rtype: typing.Text
        """
        raise NotImplementedError()

    def _repr_iterable_items(
        self, src, indent=0
    ):  # type: (typing.Iterable[typing.Any], int) -> typing.Iterator[typing.Text]
        """Repr iterable items (not designed for dicts).

        :param src: object to process
        :type src: typing.Iterable
        :param indent: start indentation
        :type indent: int
        :return: repr of element in iterable item
        :rtype: typing.Iterator[typing.Text]
        """
        for elem in src:
            yield "\n" + self.process_element(src=elem, indent=self.next_indent(indent)) + ","

    @property
    @abc.abstractmethod
    def _magic_method_name(self):  # type: () -> typing.Text
        """Magic method name.

        :rtype: typing.Text
        """
        raise NotImplementedError()

    def process_element(self, src, indent=0, no_indent_start=False):  # type: (typing.Any, int, bool) -> typing.Text
        """Make human readable representation of object.

        :param src: object to process
        :type src: typing.Any
        :param indent: start indentation
        :type indent: int
        :param no_indent_start: do not indent open bracket and simple parameters
        :type no_indent_start: bool
        :return: formatted string
        :rtype: typing.Text
        """
        if hasattr(src, self._magic_method_name):
            result = getattr(src, self._magic_method_name)(self, indent=indent, no_indent_start=no_indent_start)
            return result  # type: ignore

        if _known_callable(src):
            return self._repr_callable(src=src, indent=indent)

        if _simple(src) or indent >= self.max_indent or not src:
            return self._repr_simple(src=src, indent=indent, no_indent_start=no_indent_start)

        if isinstance(src, dict):
            prefix, suffix = "{", "}"
            result = "".join(self._repr_dict_items(src=src, indent=indent))
        else:
            if isinstance(src, list):
                prefix, suffix = "[", "]"
            elif isinstance(src, tuple):
                prefix, suffix = "(", ")"
            else:
                prefix, suffix = "{", "}"
            result = "".join(self._repr_iterable_items(src=src, indent=indent))
        return self._repr_iterable_item(
            newline=no_indent_start,
            obj_type=src.__class__.__name__,
            prefix=prefix,
            indent=indent,
            result=result,
            suffix=suffix,
        )

    def __call__(
        self, src, indent=0, no_indent_start=False
    ):  # type: (typing.Any, int, bool) -> typing.Union[six.text_type, six.binary_type]
        """Make human readable representation of object. The main entry point.

        :param src: object to process
        :type src: typing.Any
        :param indent: start indentation
        :type indent: int
        :param no_indent_start: do not indent open bracket and simple parameters
        :type no_indent_start: bool
        :return: formatted string
        :rtype: str
        """
        result = self.process_element(src, indent=indent, no_indent_start=no_indent_start)
        if self.__py2_str:  # pragma: no cover
            return result.encode(encoding="utf-8", errors="backslashreplace")
        return result


class PrettyRepr(PrettyFormat):
    """Pretty repr.

    Designed for usage as __repr__ replacement on complex objects
    """

    __slots__ = ()

    @property
    def _magic_method_name(self):  # type: () -> typing.Text
        """Magic method name.

        :rtype: typing.Text
        """
        return "__pretty_repr__"

    @staticmethod
    def _strings_repr(indent, val):  # type: (int, typing.Union[six.text_type, six.binary_type]) -> typing.Text
        """Custom repr for strings and binary strings."""
        if isinstance(val, six.binary_type):
            string = val.decode(encoding="utf-8", errors="backslashreplace")
            prefix = "b"
        else:
            prefix = "u"
            string = val
        return "{spc:<{indent}}{prefix}'''{string}'''".format(spc="", indent=indent, prefix=prefix, string=string)

    def _repr_simple(self, src, indent=0, no_indent_start=False):  # type: (typing.Any, int, bool) -> typing.Text
        """Repr object without iteration.

        :param src: Source object
        :type src: typing.Any
        :param indent: start indentation
        :type indent: int
        :param no_indent_start: ignore indent
        :type no_indent_start: bool
        :return: simple repr() over object, except strings (add prefix) and set (uniform py2/py3)
        :rtype: typing.Text
        """
        indent = 0 if no_indent_start else indent
        if isinstance(src, set):
            return "{spc:<{indent}}{val}".format(spc="", indent=indent, val="set(" + " ,".join(map(repr, src)) + ")")
        if isinstance(src, (six.binary_type, six.text_type)):
            return self._strings_repr(indent=indent, val=src)
        return "{spc:<{indent}}{val!r}".format(spc="", indent=indent, val=src)

    def _repr_dict_items(
        self, src, indent=0
    ):  # type: (typing.Dict[typing.Any, typing.Any], int) -> typing.Iterator[typing.Text]
        """Repr dict items.

        :param src: object to process
        :type src: dict
        :param indent: start indentation
        :type indent: int
        :return: repr of key/value pair from dict
        :rtype: typing.Iterator[typing.Text]
        """
        max_len = max((len(repr(key)) for key in src)) if src else 0
        for key, val in src.items():
            yield "\n{spc:<{indent}}{key!r:{size}}: {val},".format(
                spc="",
                indent=self.next_indent(indent),
                size=max_len,
                key=key,
                val=self.process_element(val, indent=self.next_indent(indent, multiplier=2), no_indent_start=True),
            )

    def _repr_callable(
        self, src, indent=0
    ):  # type: (typing.Union[types.FunctionType, types.MethodType], int) -> typing.Text
        """Repr callable object (function or method).

        :param src: Callable to process
        :type src: typing.Union[types.FunctionType, types.MethodType]
        :param indent: start indentation
        :type indent: int
        :return: Repr of function or method with signature.
        :rtype: typing.Text
        """
        param_str = ""

        for param in _prepare_repr(src):
            param_str += "\n{spc:<{indent}}{param.name}".format(spc="", indent=self.next_indent(indent), param=param)
            if param.value is not param.empty:
                param_str += "={val}".format(
                    val=self.process_element(src=param.value, indent=indent, no_indent_start=True)
                )
            param_str += ","

        if param_str:
            param_str += "\n" + " " * indent

        return "\n{spc:<{indent}}<{obj!r} with interface ({args})>".format(
            spc="", indent=indent, obj=src, args=param_str
        )

    @staticmethod
    def _repr_iterable_item(
        newline,  # type: bool
        obj_type,  # type: str
        prefix,  # type: str
        indent,  # type: int
        result,  # type: str
        suffix,  # type: str
    ):  # type: (...) -> typing.Text
        """Repr iterable item.

        :param newline: newline before item
        :type newline: bool
        :param obj_type: Object type
        :type obj_type: str
        :param prefix: prefix
        :type prefix: str
        :param indent: start indentation
        :type indent: int
        :param result: result of pre-formatting
        :type result: str
        :param suffix: suffix
        :type suffix: str
        :return: formatted repr of "result" with prefix and suffix to explain type.
        :rtype: typing.Text
        """
        return (
            "{nl}"
            "{spc:<{indent}}{obj_type:}({prefix}{result}\n"
            "{spc:<{indent}}{suffix})".format(
                nl="\n" if newline else "",
                spc="",
                indent=indent,
                obj_type=obj_type,
                prefix=prefix,
                result=result,
                suffix=suffix,
            )
        )


class PrettyStr(PrettyFormat):
    """Pretty str.

    Designed for usage as __str__ replacement on complex objects
    """

    __slots__ = ()

    @property
    def _magic_method_name(self):  # type: () -> typing.Text
        """Magic method name.

        :rtype: typing.Text
        """
        return "__pretty_str__"

    @staticmethod
    def _strings_str(indent, val):  # type: (int, typing.Union[six.text_type, six.binary_type]) -> typing.Text
        """Custom repr for strings and binary strings."""
        if isinstance(val, six.binary_type):
            string = val.decode(encoding="utf-8", errors="backslashreplace")
        else:
            string = val
        return "{spc:<{indent}}{string}".format(spc="", indent=indent, string=string)

    def _repr_simple(self, src, indent=0, no_indent_start=False):  # type: (typing.Any, int, bool) -> typing.Text
        """Repr object without iteration.

        :param src: Source object
        :type src: typing.Any
        :param indent: start indentation
        :type indent: int
        :param no_indent_start: ignore indent
        :type no_indent_start: bool
        :return: simple repr() over object, except strings (decode) and set (uniform py2/py3)
        :rtype: typing.Text
        """
        indent = 0 if no_indent_start else indent
        if isinstance(src, set):
            return "{spc:<{indent}}{val}".format(spc="", indent=indent, val="set(" + " ,".join(map(str, src)) + ")")
        if isinstance(src, (six.binary_type, six.text_type)):
            return self._strings_str(indent=indent, val=src)
        return "{spc:<{indent}}{val!s}".format(spc="", indent=indent, val=src)

    def _repr_dict_items(
        self, src, indent=0
    ):  # type: (typing.Dict[typing.Any, typing.Any], int) -> typing.Iterator[typing.Text]
        """Repr dict items.

        :param src: object to process
        :type src: dict
        :param indent: start indentation
        :type indent: int
        :return: repr of key/value pair from dict
        :rtype: typing.Iterator[typing.Text]
        """
        max_len = max((len(str(key)) for key in src)) if src else 0
        for key, val in src.items():
            yield "\n{spc:<{indent}}{key!s:{size}}: {val},".format(
                spc="",
                indent=self.next_indent(indent),
                size=max_len,
                key=key,
                val=self.process_element(val, indent=self.next_indent(indent, multiplier=2), no_indent_start=True),
            )

    def _repr_callable(
        self, src, indent=0
    ):  # type: (typing.Union[types.FunctionType, types.MethodType], int) -> typing.Text
        """Repr callable object (function or method).

        :param src: Callable to process
        :type src: typing.Union[types.FunctionType, types.MethodType]
        :param indent: start indentation
        :type indent: int
        :return: Repr of function or method with signature.
        :rtype: typing.Text
        """
        param_str = ""

        for param in _prepare_repr(src):
            param_str += "\n{spc:<{indent}}{param.name}".format(spc="", indent=self.next_indent(indent), param=param)
            if param.value is not param.empty:
                param_str += "={val}".format(
                    val=self.process_element(src=param.value, indent=indent, no_indent_start=True)
                )
            param_str += ","

        if param_str:
            param_str += "\n" + " " * indent

        return "\n{spc:<{indent}}<{obj!s} with interface ({args})>".format(
            spc="", indent=indent, obj=src, args=param_str
        )

    @staticmethod
    def _repr_iterable_item(
        newline,  # type: bool
        obj_type,  # type: str
        prefix,  # type: str
        indent,  # type: int
        result,  # type: str
        suffix,  # type: str
    ):  # type: (...) -> typing.Text
        """Repr iterable item.

        :param newline: newline before item
        :type newline: bool
        :param obj_type: Object type
        :type obj_type: str
        :param prefix: prefix
        :type prefix: str
        :param indent: start indentation
        :type indent: int
        :param result: result of pre-formatting
        :type result: str
        :param suffix: suffix
        :type suffix: str
        :return: formatted repr of "result" with prefix and suffix to explain type.
        :rtype: typing.Text
        """
        return (
            "{nl}"
            "{spc:<{indent}}{prefix}{result}\n"
            "{spc:<{indent}}{suffix}".format(
                nl="\n" if newline else "", spc="", indent=indent, prefix=prefix, result=result, suffix=suffix
            )
        )


def pretty_repr(
    src,  # type: typing.Any
    indent=0,  # type: int
    no_indent_start=False,  # type: bool
    max_indent=20,  # type: int
    indent_step=4,  # type: int
    py2_str=False,  # type: bool
):  # type: (...) -> typing.Union[six.text_type, six.binary_type]
    """Make human readable repr of object.

    :param src: object to process
    :type src: typing.Any
    :param indent: start indentation, all next levels is +indent_step
    :type indent: int
    :param no_indent_start: do not indent open bracket and simple parameters
    :type no_indent_start: bool
    :param max_indent: maximal indent before classic repr() call
    :type max_indent: int
    :param indent_step: step for the next indentation level
    :type indent_step: int
    :param py2_str: use Python 2.x compatible strings instead of unicode
    :type py2_str: bool
    :return: formatted string
    :rtype: str
    """
    return PrettyRepr(max_indent=max_indent, indent_step=indent_step, py2_str=py2_str)(
        src=src, indent=indent, no_indent_start=no_indent_start
    )


def pretty_str(
    src,  # type: typing.Any
    indent=0,  # type: int
    no_indent_start=False,  # type: bool
    max_indent=20,  # type: int
    indent_step=4,  # type: int
    py2_str=False,  # type: bool
):  # type: (...) -> typing.Union[six.text_type, six.binary_type]
    """Make human readable str of object.

    :param src: object to process
    :type src: typing.Any
    :param indent: start indentation, all next levels is +indent_step
    :type indent: int
    :param no_indent_start: do not indent open bracket and simple parameters
    :type no_indent_start: bool
    :param max_indent: maximal indent before classic repr() call
    :type max_indent: int
    :param indent_step: step for the next indentation level
    :type indent_step: int
    :param py2_str: use Python 2.x compatible strings instead of unicode
    :type py2_str: bool
    :return: formatted string
    """
    return PrettyStr(max_indent=max_indent, indent_step=indent_step, py2_str=py2_str)(
        src=src, indent=indent, no_indent_start=no_indent_start
    )
