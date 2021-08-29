from Mobel import makeDecorator, Annotation, pipeDecorators, DecoratorDefinition
from Mobel.annotation import getAnnotation, hasAnnotation


@makeDecorator
def doubler(f):
    return lambda x: f(x)*2


@makeDecorator
def multiplyBy(f, multiple=2.):
    return lambda x: f(x)*multiple


class isMultipliedBy(Annotation):

    multipliedBy: float = 3.


pipedDecorators = pipeDecorators([
    DecoratorDefinition(doubler),
    DecoratorDefinition(multiplyBy, ["multiple"]),
    DecoratorDefinition(isMultipliedBy, ["multipliedBy"])
])

mappedDecorators = pipeDecorators([
    DecoratorDefinition(doubler),
    DecoratorDefinition(multiplyBy, ["multiple"]),
    DecoratorDefinition(isMultipliedBy, ["multipliedBy"], {
                        "multiple": "multipliedBy"})
])


class TestPipe:
    """Pipe:
    """

    def test_pipeWithArguments(self):
        @pipedDecorators(multiple=10., multipliedBy=4.)
        def identity(x):
            return x

        assert identity(1) == 20
        assert hasAnnotation(identity, isMultipliedBy)
        assert getAnnotation(identity, isMultipliedBy).multipliedBy == 4.

    def test_pipeWithArgumentsForOneDecorator(self):
        @pipedDecorators(multiple=10.)
        def identity(x):
            return x

        assert identity(1) == 20
        assert hasAnnotation(identity, isMultipliedBy)
        assert getAnnotation(identity, isMultipliedBy).multipliedBy == 3.

    def test_pipeWithNoArguments(self):
        @pipedDecorators
        def identity(x):
            return x

        assert identity(1) == 4
        assert hasAnnotation(identity, isMultipliedBy)
        assert getAnnotation(identity, isMultipliedBy).multipliedBy == 3.

    def test_pipeMapping(self):
        @mappedDecorators(multiple=10.)
        def identity(x):
            return x

        assert identity(1) == 20
        assert hasAnnotation(identity, isMultipliedBy)
        assert getAnnotation(identity, isMultipliedBy).multipliedBy == 10.
