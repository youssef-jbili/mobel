from Mobel import Annotation
from Mobel.annotation import getAnnotation, hasAnnotation

import pytest


class TestAnnotation:
    """Annotation:
    """

    def test_AddAndCheckAnnotation(self):
        """should create Annotation and check that it's present
        """

        class TestAnnotation(Annotation):
            pass

        @TestAnnotation
        def testFunction():
            pass  # ignore: S1186

        assert hasAnnotation(testFunction, "TestAnnotation")
        assert not hasAnnotation(testFunction, "SomeOtherAnnotation")

    def test_AddAndRecoverAnnotation(self):
        """should create Annotation and get its parameters
        """

        class TestAnnotation(Annotation):
            testValue: float

        @TestAnnotation(testValue=4.)
        def testFunction():
            pass  # ignore: S1186

        assert getAnnotation(testFunction, TestAnnotation).testValue == 4.

    def test_CheckAnnotationOnVanillaFunction(self):
        """hasAnnotation should work on vanilla functions
        """

        def testFunction():
            pass  # ignore: S1186

        assert not hasAnnotation(testFunction, "SomeAnnotation")

    def test_getAnnotationOnVanillaFunction(self):
        """getAnnotation should work on vanilla functions
        """

        class SomeAnnotation(Annotation):
            pass

        def testFunction():
            pass  # ignore: S1186

        assert getAnnotation(testFunction, SomeAnnotation) is None

    def test_functionHasMultipleAnnotations(self):
        """test function that contains multiple annotations
        """

        class FirstAnnotation(Annotation):
            pass

        class SecondAnnotation(Annotation):
            pass

        @FirstAnnotation
        @SecondAnnotation
        def testFunction():
            pass  # ignore: S1186

        assert hasAnnotation(testFunction, "FirstAnnotation")
        assert hasAnnotation(testFunction, "SecondAnnotation")

    def test_callDecoratorWithoutArgumentsRaisesError(self):
        """should raise ValueError if an annotation that requires arguments
            doesn't get them
        """

        class FirstAnnotation(Annotation):
            required: bool

        with pytest.raises(TypeError):

            @FirstAnnotation
            def testFunction():
                pass  # ignore: S1186
