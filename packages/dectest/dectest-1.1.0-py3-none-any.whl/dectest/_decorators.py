from typing import TypeVar, Callable
import unittest

from ._types import TestMethod

_F = TypeVar("_F", bound=TestMethod)


def test(method: _F) -> _F:
    """Decorator that flags a method as a test method."""
    method._dectest_test = True  # type: ignore
    return method


def before(method: _F) -> _F:
    """Decorator that flags a method as fixture setup.

    Fixture setup methods from base classes are guaranteed to be executed
    before setup methods from derived classes.
    """
    method._dectest_before = True  # type: ignore
    return method


def after(method: _F) -> _F:
    """Decorator that flags a method as fixture teardown.

    Fixture teardown methods from base classes are guaranteed to be executed
    after teardown methods from derived classes.
    """
    method._dectest_after = True  # type: ignore
    return method


def skip(reason: str) -> Callable[[_F], _F]:
    """Unconditionally skip the decorated test.

    This is equivalent to @unittest.skip, but also marks the decorated
    function as a test.
    """

    if not isinstance(reason, str):
        raise TypeError("first argument to @skip must be a reason string")

    def decorate(method: _F) -> _F:
        return unittest.skip(reason)(test(method))

    return decorate


def skip_if(condition: bool, reason: str) -> Callable[[_F], _F]:
    """Skip the decorated test if condition is true.

    This is equivalent to @unittest.skipIf, but also marks the decorated
    function as a test.
    """

    def decorate(method: _F) -> _F:
        return unittest.skipIf(condition, reason)(test(method))

    return decorate


def skip_unless(condition: bool, reason: str) -> Callable[[_F], _F]:
    """Skip the decorated test unless condition is true.

    This is equivalent to @unittest.skipUnless, but also marks the decorated
    function as a test.
    """

    def decorate(method: _F) -> _F:
        return unittest.skipUnless(condition, reason)(test(method))

    return decorate
