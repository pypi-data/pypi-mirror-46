# __Limitloop__

Limitloop is a lightweight python module for running loops that depend on precise timing.

This package is available through Pypi and can be installed with the following command.

```sh
python -m pip install limitloop
```

## Basic usage

All functionality of the module is provided through the `limitloop.Loop` class. This class is instantiated with a reference to a function, which it can then call at a consistent rate a preset number of times, or until otherwise interrupted. For example, the following code...

```python
from limitloop import Loop

#Define a simple function for the Loop object to call
#This function must accept the loop object itself as its first argument
def demoFunction(loop):
    print('Hello, world!')

#Create our loop object, set to run at one iteration per second
l = Loop(demoFunction, freq=1)
#Call the function defined above 5 times
l.run(5)
```
...will output the following, one line per second.
```
Hello, world!
Hello, world!
Hello, world!
Hello, world!
Hello, world!
```
See the [API reference](api_reference.md) for more advanced usage.

*TODO: Add more advanced usage examples*
