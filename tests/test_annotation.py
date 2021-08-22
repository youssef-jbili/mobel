from Mobel import Annotation, makeDecorator
from Mobel.annotation import hasAnnotation


class TestAnnotation:
    """Annotation:
    """

    def test_AddAndRecoverAnnotation(self):
        """should create Annotation and check that it's present
        """

        class TestAnnotation(Annotation):
            pass

        @TestAnnotation
        def testFunction():
            pass  # ignore: S1186

        assert hasAnnotation(testFunction, "TestAnnotation") == True
        assert hasAnnotation(testFunction, "SomeOtherAnnotation") == False

    def test_CheckAnnotationOnVanillaFunction(self):
        """getAnnotation should work on vanilla functions
        """

        def testFunction():
            pass  # ignore: S1186

        assert hasAnnotation(testFunction, "SomeAnnotation") == False

    def test_DecoratorsPreserveAnnotations(self):
        """decorators should preserve annotations
        """

        class TestAnnotation(Annotation):
            pass

        @makeDecorator
        def testDecorator(_):
            def anotherFunction():
                pass  # ignore: S1186
            return anotherFunction

        @testDecorator
        @TestAnnotation
        def testFunction():
            pass  # ignore: S1186

        assert hasAnnotation(testFunction, "TestAnnotation") == True
