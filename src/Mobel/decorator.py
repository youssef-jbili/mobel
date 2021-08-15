from inspect import signature
from typing import TypeVar, Callable, overload
from functools import wraps

__all__ = ["makeDecorator"]

TA = TypeVar("TA")
TB = TypeVar("TB")
TC = TypeVar("TC")
TD = TypeVar("TD")
TE = TypeVar("TE")
TF = TypeVar("TF")
TG = TypeVar("TG")
TH = TypeVar("TH")
TI = TypeVar("TI")
TJ = TypeVar("TJ")

F = TypeVar("F", bound=Callable)

RV = TypeVar("RV")

Decorator = Callable[[F], RV]
NoArgsDecoratorFactory = Callable[[], Decorator]

PA = Callable[[F, TA], RV]
DA = Callable[[TA], Decorator]

PB = Callable[[F, TA, TB], RV]
DB = Callable[[TA, TB], Decorator]

PC = Callable[[F, TA, TB, TC], RV]
DC = Callable[[TA, TB, TC], Decorator]

PD = Callable[[F, TA, TB, TC, TD], RV]
DD = Callable[[TA, TB, TC, TD], Decorator]

PE = Callable[[F, TA, TB, TC, TD, TE], RV]
DE = Callable[[TA, TB, TC, TD, TE], Decorator]


@overload
def makeDecorator(decoratorPrototype: Decorator) -> NoArgsDecoratorFactory:
    ...  # pragma: no cover


@overload
def makeDecorator(decoratorPrototype: PA) -> DA:
    ...  # pragma: no cover


@overload
def makeDecorator(decoratorPrototype: PB) -> DB:
    ...  # pragma: no cover


@overload
def makeDecorator(decoratorPrototype: PC) -> DC:
    ...  # pragma: no cover


@overload
def makeDecorator(decoratorPrototype: PD) -> DD:
    ...  # pragma: no cover


@overload
def makeDecorator(decoratorPrototype: PE) -> DE:
    ...  # pragma: no cover


def makeDecorator(decoratorPrototype):
    def decoratorFactory(*args, **kwargs):
        def decorator(functionToDecorate):
            return wraps(functionToDecorate)(decoratorPrototype(functionToDecorate, *args, *kwargs))
        return decorator
    return decoratorFactory
