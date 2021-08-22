from typing import Callable
from Mobel import makeDecorator
import pytest


class TestDecorator:
    """Decorator:
    """

    def test_DecoratorWithArgsPresent(self):
        """should make a decorator factory when the decorator prototype requires arguments
        and arguments are supplied
        """

        @makeDecorator
        def dummyDecorator(f: Callable, multiplier: float = 2.) -> Callable:
            def decorator(*args, **kwargs):
                return multiplier*f(*args, **kwargs)
            return decorator

        @dummyDecorator(multiplier=3)
        def targetFunction(x: float):
            return 2*x

        assert targetFunction(1) == 6

    def test_DecoratorWithArgsAbsent(self):
        """should make a decorator when the decorator prototype requires arguments
        and arguments are absent
        """

        @makeDecorator
        def dummyDecorator(f: Callable, multiplier: float = 2.) -> Callable:
            def decorator(*args, **kwargs):
                return multiplier*f(*args, **kwargs)
            return decorator

        @dummyDecorator
        def targetFunction(x: float):
            return 2*x

        assert targetFunction(1) == 4

    def test_ArgsDecorator(self):
        """should convert normal decorators to decorator factories if needed
        """

        @makeDecorator
        def dummyDecorator(f: Callable) -> Callable:
            def decorator(*args, **kwargs):
                return 2*f(*args, **kwargs)
            return decorator

        @dummyDecorator()
        def targetFunction(x: float):
            return 2*x

        assert targetFunction(1) == 4

    def test_PrototypeWithPositionalOnlyArguments(self):
        """should raise an error if the prototype has positional only arguments
        """

        def dummyDecorator(f, x, /):
            pass  # ignore S1186

        with pytest.raises(ValueError):
            makeDecorator(dummyDecorator)

    def test_PrototypeWithNoArguments(self):
        """should raise an error if the prototype has no arguments
        """

        def dummyDecorator():
            pass  # ignore S1186

        with pytest.raises(ValueError):
            makeDecorator(dummyDecorator)
