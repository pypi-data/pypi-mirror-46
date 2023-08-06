Assorted decorator functions.


Assorted decorator functions.

## Function `decorator(deco)`

Wrapper for decorator functions to support optional arguments.
The actual decorator function ends up being called as:

    deco(func, *da, **dkw)

allowing `da` and `dkw` to affect the bahviour of the decorator `deco`.

Examples:

    @decorator
    def deco(func, *da, kw=None):
      ... decorate func subject to the values of da and kw
    @deco
    def func1(...):
      ...
    @deco('foo', arg2='bah')
    def func2(...):
      ...

## Function `fmtdoc(func)`

Decorator to replace a function's docstring with that string
formatted against the function's module's __dict__.

This supports simple formatted docstrings:

    ENVVAR_NAME = 'FUNC_DEFAULT'

    @fmtdoc
    def func():
        """Do something with os.environ[{ENVVAR_NAME}]."""
        print(os.environ[ENVVAR_NAME])

This gives `func` this docstring:

    Do something with os.environ[FUNC_DEFAULT].

*Warning*: this decorator is intended for wiring "constants"
into docstrings, not for dynamic values. Use for other types
of values should be considered with trepidation.

## Function `observable_class(property_names, only_unequal=False)`

Class decorator to make various instance attributes observable.

Parameters:
* `property_names`:
  an interable of instance property names to set up as
  observable properties. As a special case a single `str` can
  be supplied of only one attribute is to be observed.
* `only_unequal`:
  only call the observers if the new property value is not
  equal to the previous proerty value. This requires property
  values to be comparable for inequality.
  Default: `False`, meaning that all updates will be reported.
