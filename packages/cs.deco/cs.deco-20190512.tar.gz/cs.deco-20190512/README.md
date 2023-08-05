Assorted decorator functions.


Assorted decorator functions.

## Function `cached(*da, **dkw)`

Decorator to cache the result of a method and keep a revision
counter for changes.

The cached values are stored on the instance (`self`).
The revision counter supports the `@revised` decorator.

This decorator may be used in 2 modes.
Directly:

    @cached
    def method(self, ...)

or indirectly:

    @cached(poll_delay=0.25)
    def method(self, ...)

Optional keyword arguments:
* `attr_name`: the basis name for the supporting attributes.
  Default: the name of the method.
* `poll_delay`: minimum time between polls; after the first
  access, subsequent accesses before the `poll_delay` has elapsed
  will return the cached value.
  Default: `None`, meaning no poll delay.
* `sig_func`: a signature function, which should be significantly
  cheaper than the method. If the signature is unchanged, the
  cached value will be returned. The signature function
  expects the instance (`self`) as its first parameter.
  Default: `None`, meaning no signature function;
  the first computed value will be kept and never updated.
* `unset_value`: the value to return before the method has been
  called successfully.
  Default: `None`.

If the method raises an exception, this will be logged and
the method will return the previously cached value,
unless there is not yet a cached value
in which case the exception will raise.

If the signature function raises an exception
then a log message is issued and the signature is considered unchanged.

An example use of this decorator might be to keep a "live"
configuration data structure, parsed from a configuration
file which might be modified after the program starts. One
might provide a signature function which called `os.stat()` on
the file to check for changes before invoking a full read and
parse of the file.

## Function `decorator(deco)`

Wrapper for decorator functions to support optional keyword arguments.

Examples:

    @decorator
    def dec(func, **dkw):
      ...
    @dec
    def func1(...):
      ...
    @dec(foo='bah')
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

## Function `strable(*da, **dkw)`

Decorator for functions which may accept a `str`
instead of their core type.

Parameters:
* `func`: the function to decorate
* `open_func`: the "open" factory to produce the core type form
  the string if a string is provided; the default is the builtin
  "open" function

The usual (and default) example is a function to process an
open file, designed to be handed a file object but which may
be called with a filename. If the first argument is a `str`
then that file is opened and the function called with the
open file.

Examples:

    @strable
    def count_lines(f):
      return len(line for line in f)

    class Recording:
      "Class representing a video recording."
      ...
    @strable
    def process_video(r, open_func=Recording):
      ... do stuff with `r` as a Recording instance ...
