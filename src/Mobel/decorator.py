from typing import Callable, Optional, TypeVar, overload
import inspect
from functools import wraps

__all__ = "makeDecorator"

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
    function_signature = inspect.signature(decoratorPrototype)

    if len(function_signature.parameters.values()) == 0:
        raise ValueError("decorator prototype must have at least one argument")

    if functionHasPositionalOnlyArguments(function_signature):
        raise ValueError(
            "decorator prototype can't have positional only arguments")

    def decoratorOrFactory(functionToDecorate: Optional[Callable] = None, /, **kwargs):
        if functionToDecorate is None:
            def decorator(functionToDecorate):
                return wraps(functionToDecorate)(decoratorPrototype(functionToDecorate, **kwargs))
            return decorator
        return wraps(functionToDecorate)(decoratorPrototype(functionToDecorate))
    return decoratorOrFactory


def functionHasPositionalOnlyArguments(function_signature: inspect.Signature) -> bool:
    arguments = iter(function_signature.parameters.values())
    next(arguments)  # skip the first argument which is the function to decorate
    try:
        first_argument = next(arguments)
        return first_argument.kind == first_argument.POSITIONAL_ONLY
    except StopIteration:
        return False
