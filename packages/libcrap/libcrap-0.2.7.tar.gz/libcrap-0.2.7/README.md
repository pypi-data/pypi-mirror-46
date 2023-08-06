libcrap
=======

A library of useful functions, classes and other pieces of code
which I want to use in almost every project I make.

It does not work with python 2.


Installation
------------

```
pip install --user libcrap
```

If you also want to use **pytorch** stuff, use `torch` installation flag
```
pip install --user libcrap[torch]
```

And if you want to be able to run tests and check typing, use flags `dev` and `test`
```
pip install --user libcrap[dev,test]
```

If you've cloned this repository somewhere and want to install libcrap in editable mode,
do

```shell
$ cd /my/projects/directory/libcrap
$ pip install --editable .[dev,test,torch]
```

## Run Tests and Check Typing

This library uses **pytest** for testing and [mypy](http://mypy-lang.org/)
for typechecking.

```shell
$ cd /my/projects/directory/libcrap
$ make check_all  # it will run mypy to check types and run tests with pytest
```


Modules
-------

### core.py

Different stuff

### visualization.py

#### Distinguishable Colors

A python function that provides N distinguishable colors. Can be used for multiple plots in the same figure or something like that.

![Distinguishable Colors](https://i.stack.imgur.com/pFuNR.png)

```python
from libcrap.visualization import get_distinguishable_colors

print(get_distinguishable_colors(7))
# ['#0000ff', '#ff0000', '#00ff00', '#00002b', '#ff1ab8', '#ffd300', '#005700']

print(get_distinguishable_colors(-3)) # this is stupid -> Error

print(get_distinguishable_colors(123456)) # too many, not supported -> Error
```

### torch.py

Stuff that uses **pytorch**.