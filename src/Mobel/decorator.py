from inspect import signature
from typing import TypeVar, Callable, overload

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

PNone = Callable[[F], RV]
DNone = Callable[[], RV]

PA = Callable[[F, TA], RV]
DA = Callable[[TA], RV]

PB = Callable[[F, TA, TB], RV]
DB = Callable[[TA, TB], RV]

PC = Callable[[F, TA, TB, TC], RV]
DC = Callable[[TA, TB, TC], RV]

PD = Callable[[F, TA, TB, TC, TD], RV]
DD = Callable[[TA, TB, TC, TD], RV]

PE = Callable[[F, TA, TB, TC, TD, TE], RV]
DE = Callable[[TA, TB, TC, TD, TE], RV]


@overload
def makeDecorator(f: PNone) -> DNone:
    ...  # pragma: no cover


@overload
def makeDecorator(f: PA) -> DA:
    ...  # pragma: no cover


@overload
def makeDecorator(f: PB) -> DB:
    ...  # pragma: no cover


@overload
def makeDecorator(f: PC) -> DC:
    ...  # pragma: no cover


@overload
def makeDecorator(f: PD) -> DD:
    ...  # pragma: no cover


@overload
def makeDecorator(f: PE) -> DE:
    ...  # pragma: no cover


def makeDecorator(decoratorPrototype):

    numberOfTemplateArguments = numberOfArguments(decoratorPrototype)

    if numberOfTemplateArguments == 1:
        raise ValueError(
            """expected decorator to take more than one argument, 
            for simple decorators 'makeDecorator' is not needed""")

    def decoratorFactory(*args, **kwargs):
        def decorator(functionToDecorate):
            return decoratorPrototype(functionToDecorate, *args, *kwargs)
        return decorator
    return decoratorFactory


def numberOfArguments(f: Callable) -> int:
    return len(signature(f).parameters)
