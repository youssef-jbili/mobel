# Documentation

### Basic decorator

The standard python method to implement decorator factories can be a bit cumbersome. It also means a decorator factory cannot be used as a decorator.
Mobel attempts to solve both these problems using the `makeDecorator` function. It takes a decorator prototype and converts it into a function that can be used as either 
a decorator or a decorator factory.

It can be used simply by adding it as a decorator to decorator prototype, which is a function that takes another function to decorate and some arguments which it can get
if used as a decorator factory

``` Python

# Definition of decorator

@makeDecorator
def multiplyResult(f,factor=3):
  return lambda x:factor*f(x)
  
# Usage  
 
@multiplyResult 
def identity1(x):
  return x

print(identity1(1)) # 3

@multiplyResult(factor=2)
def identity2(x):
  return x

print(identity2(1)) # 2
```

This flexibility comes at a small cost: decorators can only take keyword arguments. if the decorator is called with a positional argument it will mistake it
for the function to decorate. This also means that if the decoratory prototype contains a positional only argument other than the function to decorate, it will throw an Exception

### Annotations 

Some times you might want to mark a function in some way to reflect that it exhibits a certain property of interest. This can be implemented using `Annotation`

``` Python

# Definition

class mySuperAnnotation(Annotation):
    numberOfThings:int = 5
   
# Usage

@mySuperAnnotation(numberOfThings = 3)
def dummyFunction():
    ...

hasAnnotation(dummyFunction,mySuperAnnotation) # True
getAnnotation(dummyFunction,mySuperAnnotation).numberOfThings # 3

@mySuperAnnotation
def otherDummyFunction():
    ...

getAnnotation(otherDummyFunction,mySuperAnnotation).numberOfThings # 5
```

Internally it uses the Python `dataclass` to store the annotation data

### Pipes

If you have many decorators and you want to group them into one decorator that handles all their arguments, you can make a decorator Pipe. To ensure that each decorator
can get its own arguments from the arguments supplied to the piped decorator, the pipeDecorators function requires information about the decorator. This information comes in
the form of a `DecoratorDefinition`, which takes the following arguments:
- the decorator (obviously)
- the list of named arguments that the decorator can accept (if it has arguments)
- a dictionnary that defines mapping from the global arguments to the decorator arguments. It can be useful if 2 decorators don't share argument names but you want to link them in a particular pipe

``` Python


pipedDecorators = pipeDecorators([
    # decorator with no arguments
    DecoratorDefinition(decorator1),
    # decorator that takes only one argument "arg1"
    DecoratorDefinition(decorator2, ["arg1"]),
    # decorator that takes only one argument "arg2", that is mapped from "arg1"
    DecoratorDefinition(decorator3, ["arg2"], {"arg1": "arg2"})
])

```
