from typing import Callable
from Mobel import makeDecorator
import pytest


class TestMobel:
    """Mobel:
    """

    def test_makeDecorator(self):
        """should make a valid decorator
        """

        @makeDecorator
        def dummyDecorator(f: Callable, multiplier: float) -> Callable:
            def decorator(*args, **kwargs):
                return multiplier*f(*args, **kwargs)
            return decorator

        @dummyDecorator(3)
        def targetFunction(x: float):
            return 2*x

        assert targetFunction(1) == 6

    def test_NoArgsDecorator(self):
        """should convert normal decorators to decorator factories
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
