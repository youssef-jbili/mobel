from typing import Callable, Optional, TypeVar, Union, overload, Protocol
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

F = TypeVar("F", bound=Callable, contravariant=True)

RV = TypeVar("RV", bound=Callable, covariant=True)

Decorator = Callable[[F], RV]
NoArgsDecoratorFactory = Callable[[], Decorator]


class DecoratorFactory(Protocol[F, RV]):
    @overload
    def __call__(self) -> Callable[[F], RV]: ...
    @overload
    def __call__(self, f: F) -> RV: ...


PA = Callable[[F, TA], RV]
DA = Union[Callable[[TA], Decorator], DecoratorFactory[F, RV]]

PB = Callable[[F, TA, TB], RV]
DB = Union[Callable[[TA, TB], Decorator], DecoratorFactory[F, RV]]

PC = Callable[[F, TA, TB, TC], RV]
DC = Union[Callable[[TA, TB, TC], Decorator], DecoratorFactory[F, RV]]

PD = Callable[[F, TA, TB, TC, TD], RV]
DD = Union[Callable[[TA, TB, TC, TD], Decorator], DecoratorFactory[F, RV]]

PE = Callable[[F, TA, TB, TC, TD, TE], RV]
DE = Union[Callable[[TA, TB, TC, TD, TE], Decorator], DecoratorFactory[F, RV]]


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
