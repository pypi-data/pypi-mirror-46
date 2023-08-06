renew
=====

| Semi-text-pickling in pure python.
| If you meet just a few restrictions, you can store classes
| state into a python file and import or evaluate it somewhere
| else or later on. You can even use it as a database unless
| the amount of data is huge.

1 minute - example:
~~~~~~~~~~~~~~~~~~~

.. code:: python

    import renew 

    class ThatNiceClass(renew.Mold):
        # manual implementation of __init__ is needed. Constructor_arguments
        # have to be actual names of this class attributes
        def __init__(self, f_a, f_b, *f_c, **f_d):
            self.f_a, self.f_b, self.f_c, self.f_d = f_a, f_b, f_c, f_d

    c = ThatNiceClass(1, 2, 3, 4, five=5, six=6)

    assert repr(c) == "ThatNiceClass(1, 2, 3, 4, five=5, six=6)"
    assert c == eval(repr(c))  # __eq__ implemented 
    assert repr(c) == repr(eval(repr(c)))  # pure reproduction, instance "survives" eval

    class SecondClass(renew.Mold):
        _cls_namespace = "foo_pkg"

        def __init__(self, one, two="number two", three=None):
            self.one, self.two, self.three = one, two, three

    s1 = SecondClass(1)
    s2 = SecondClass(3.14159, "non default")
    s3 = SecondClass("Lorem ipsum dolor sit amet, consectetur adipiscing elit")
    s4 = SecondClass(4, three=ThatNiceClass(1, 2, 3, 4, five=5, six=6))

    d = ThatNiceClass(s1, s2, lorem=s3, im_nesting=s4)

    assert repr(d) == """\
    ThatNiceClass(
        foo_pkg.SecondClass(1),
        foo_pkg.SecondClass(3.14159, 'non default'),
        im_nesting=foo_pkg.SecondClass(4, three=ThatNiceClass(1, 2, 3, 4, five=5, six=6)),
        lorem=foo_pkg.SecondClass('Lorem ipsum dolor sit amet, consectetur adipiscing elit'),
    )"""

The ``__repr__`` story - repr(object)
-------------------------------------

| Does ``repr`` stand for "representation" or "reproduction"?
| According to python documentation ``__repr__`` functionality has two
| separate approaches. From
  https://docs.python.org/3/library/functions.html#repr (v 3.7.2)

    | ``repr(object)`` Return a string containing a printable
      representation of an object.
    | For many types, this function makes an attempt to return a string
    | that would yield an object with the same value when passed to
      eval(),
    | otherwise the representation is a string enclosed in angle
      brackets
    | that contains the name of the type of the object together with
    | additional information often including the name and address of
    | the object. A class can control what this function returns for
    | its instances by defining a ``__repr__()`` method.

1. reproducible repr:
---------------------

| For several native objects it returns a string that can be used
| to reproduce given object, i.e. to create a copy of given object.

.. code:: python

    a = [1, 3.141559, None, "string"]
    statement_str = repr(a)
    assert statement_str == '[1, 3.141559, None, "string"]'

You may tell that repr of an object is ``reproducible`` if this is meet:

.. code:: python

    a = [1, 3.14159, None, "string"]
    statement_str = repr(a)
    assert repr(eval(statement_str)) == statement_str
    # if the object implements __eq__ this should be also true:
    assert eval(statement_str) == a

2. descriptive repr:
--------------------

| Unfortunately python does not serve the "reproducible repr" out of the
  box
| for types defined by user:

.. code:: python

    class Car(object):
        def __init__(self, body_type, engine_power):
            self.body_type = body_type
            self.engine_power = engine_power

    car = Car("coupe", 124.0)
    # repr(car) == '<__main__.Car object at 0x7f0ff6313290>'
    # but using renew:

    import renew

    class ReproducibleCar(renew.Mold):
        _cls_namespace = "bar"
        def __init__(self, body_type, engine_power):
            self.body_type = body_type
            self.engine_power = engine_power

    car2 = ReproducibleCar("sedan", 110.0)
    assert repr(car2) == 'bar.ReproducibleCar("sedan", 110.0)'

The method above is implemented as a decorator, but you can also use a
inheritance to get the same result.

.. code:: python

    import renew

    class Car(renew.Mold):
        _cls_namespace = "cars"
        _cls_dependency = "that.things"

        def __init__(self, body_type, engine_power, fuel, seats, color=None):
            self.body_type = body_type
            self.engine_power = engine_power
            self.fuel = fuel
            self.seats = seats
            self.color = color

    class Driver(renew.Mold):
        _cls_namespace = "persons"

        def __init__(self, first_name, last_name, *cars):
            self.first_name = first_name
            self.last_name = last_name
            self.cars = cars

    car_1 = Car("Truck", 120.0, "diesel", 2)
    car_2 = Car("Van", 145.0, "diesel", seats=7, color="silver")
    car_3 = Car("Roadster", 210.0, "gasoline", seats=2)

    driver_1 = Driver("Blenda", "Klapa", car_1)
    driver_2 = Driver("Trytka", "Blotnick", car_2, car_3)

    assert repr(driver_1) == ".Driver('Blenda', 'Klapa', cars.Car('Truck', 120.0, 'diesel', 2))"
    assert repr(driver_2) == """\
    persons.Driver(
        'Trytka',
        'Blotnick',
        cars.Car('Van', 145.0, 'diesel', 7, 'silver'),
        cars.Car('Roadster', 210.0, 'gasoline', 2),
    )"""

    renew.serialize("/tmp/target.py", blenda=driver_1, trytka=driver_2)

The created file looks like this:

.. code:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    # This file has been created with renew.
    # A py-pickling tool: https://pypi.org/project/renew/

    from living.things import persons
    from that.things import cars

    blenda = persons.Driver('Blenda', 'Klapa', cars.Car('Truck', 120.0, 'diesel', 2))

    trytka = persons.Driver(
        'Trytka',
        'Blotnick',
        cars.Car('Van', 145.0, 'diesel', 7, 'silver'),
        cars.Car('Roadster', 210.0, 'gasoline', 2),
    )

How it works?
-------------

| Note that ``ReproducibleCar`` does not explicitly implement the
  ``__repr__``, but the ``renew.reproducible``
| decorator supplements it (overrides it if any has been defined
  before).
| ``renew.reproduction`` inspects constructor's argument specification
| of decorated class and yields a string that tries to be a call
  statement composed of

-  ``namespace``, e.g. your package name (according to desired importing
   convention)
-  given class name
-  given class' attributes values, that have the same names and order as
   constructor arguments

That forms the only one usage restriction:

**The class has to store all the constructor arguments in its attributes
with the same
name** (as in ``ReproducibleCar`` definition above).

| Variadic args have to be stored in the instance either as ``list``,
  ``tuple`` (no cast needed), ``set`` or ``OrderedDict``
| (set is rendered with sorting). Keyword args have to be stored in the
  instance as a ``dict`` or ``OrderedDict``.

.. code:: python

    from collections import OrderedDict
    import renew

    class ThatClass(renew.Mold):
        def __init__(self, x=1, *others, **kw_args):
            self.x = x
            self.others = OrderedDict(others)
            self.kw_args = kw_args

    that = ThatClass(3.14159, ("a", "A"), ("b", "B"), one=1, two=2, many=666)

    assert repr(that) == "ThatClass(3.14159, many=666, one=1, two=2)"
    assert that.x == 3.14159
    assert that.others == OrderedDict([("a", "A"), ("b", "B")])
    assert that.kw_args == dict(one=1, two=2, many=666)
     

Limitations
-----------

-  keys of plain ``dict`` being "complex" objects get a bit ugly layout
   if repr of given key spans multiple lines.
-  | ``renew`` does not cross-reference objects while serializing.
   | Although neither ``pickle`` nor ``marshal`` does cross-reference,
     ``renew`` most probably could do it but it's
   | hard to tell how to let renew know where and how a chain of objects
     have to be cross-referenced.

-  For ultra-capable meta programming ``MacroPy``:
   https://pypi.org/project/MacroPy/ would be a better choice.

For full list of features and usage examples, please refer to unit
tests, especially ``tests/test_renew.py``.
