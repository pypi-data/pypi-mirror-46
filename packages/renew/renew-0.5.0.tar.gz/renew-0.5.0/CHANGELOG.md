# CHANGELOG
The story begins at early february 2019

### 0.1 - initial release
* supported arguments: positional, variadic and default 
* interfaces: `reproduction_string` function and `reproducible` decorator

#### 0.1.1 - minor improvements
* `reproduction_string` can take arbitrary instance and try to evaluate its *nice repr* at runtime
* project hosted on gitlab

### 0.2 - slight interface change
* `reproduction_string` function renamed to `reproduction`
* adding tox env for python 3.7 
#### 0.2.1 - kitchen work
* package's readme back in `rst` format (less environmental mess)
* adding tox env pypy
#### 0.2.2
* remove wrapping long string with brackets if it's not
called on top-level in passed object tree
* code coverage raised up to 94%

### 0.3.0 - adding serializer and changing interface 
* interface changed `reproducible` becomes reserved for a base object
implementing `renew` methods, it's renamed to `make_renew_reprs` 
* adding inheritance extension
* adding serialization helper
* testenv: adding coverage measurement
#### 0.3.1
* allowing `renew.serialize` to accept both - positional and keyword arguments
#### 0.3.2  `**kwargs`
* renew supports keyword-arguments

### 0.4 Changed interface and usage.
#### 0.4.0
Reproducible objects are now created by deriving from `renew.Mold` class. 
The project has been almost rewritten.
* decorating functionality `make_renew_reprs` is removed
* each `renew.Mold` subclass gets implementations of:
  - `__repr__`, `__eq__`, `__ne__`, `__hash__`
  - `__len__`, `__iter__` work as in namedtuple, instance can be unpacked, 
  iterated or casted to iterable
  - `__slots__` are automatically assigned to each subclass
  - class' `namespace` and `dependency` attributes are inherited in 
  natural *pythonic* way (no *abracadabra* anymore)
* fixed `namedtuple`' repr implementation 

#### 0.4.1
adding `_cls_make_slots` class attribute setting to
disable `__slots__` creation
#### 0.4.2 & 0.4.3
* fixing `OrderedDict` repr fail in variadic args
* fixing implementation of `__eq__` in derived classes
(0.4.2==0.4.3 because of pypi issue, failed to upload the file for second time, my fault)
#### 0.4.4
* adding `_extra_slots` field that allows for defining slots ignored
in constructor and eq operations.
#### 0.4.5
* fixing repr of tuples containing single element.
There was missing comma, eg: `'(4)'` instead of `'(4,)'`
#### 0.4.6
* adding proper repr of OrderedDict
* fixing repr of empty sets
#### 0.4.7
* fixing repr or long string wrapped into multiple lines
  (in some cases comma was missing at the end of last line)

### 0.5
#### 0.5.0
* Adding serialization helpers (PyStorage) that can dump data to and load from a disk.
* A bit better handling of unicode strings (there is most probably still place for corrections)
