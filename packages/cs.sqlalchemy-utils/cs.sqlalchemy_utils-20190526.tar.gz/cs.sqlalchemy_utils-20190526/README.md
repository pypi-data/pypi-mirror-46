Assorted utility functions to support working with SQLAlchemy.


Assorted utility functions to support working with SQLAlchemy.

## Function `auto_session(func)`

Decorator to run a function in a session is not presupplied.

## Function `find_json_field(column_value, field_name, *, infill=False)`

Descend a JSONable Python object `column_value`
to `field_name`.
Return `column_value` (possibly infilled), `final_field`, `final_field_name`.

This supports database row columns which are JSON columns.

Parameters:
* `column_value`: the original value of the column
* `field_name`: the field within the column to locate
* `infill`: optional keyword parameter, default `False`.
  If true,
  `column_value` and its innards will be filled in as `dict`s
  to allow deferencing the `field_name`.

The `field_name` is a `str`
consisting of a period (`'.'`) separated sequence of field parts.
Each field part becomes a key to index the column mapping.
These keys are split into the leading field parts
and the final field part,
which is returned as `final_field_name` above.

The `final_field` return value above
is the mapping within which `final_field_value` may lie
and where `final_field_value` may be set.
Note: it may not be present.

If a leading key is missing and `infill` is true
the corresponding part of the `column_value` is set to an empty dictionary
in order to allow deferencing the leading key.
This includes the case when `column_value` itself is `None`,
which is why the `column_value` is part of the return.

If a leading key is missing and `infill` is false
this function will raise a `KeyError`
for the portion of the `field_name` which failed.

Examples:

    >>> find_json_field({'a':{'b':{}}},'a.b')
    ({'a': {'b': {}}}, {'b': {}}, 'b')
    >>> find_json_field({'a':{}},'a.b')
    ({'a': {}}, {}, 'b')
    >>> find_json_field({'a':{'b':{}}},'a.b.c.d')
    Traceback (most recent call last):
        ...
    KeyError: 'a.b.c'
    >>> find_json_field({'a':{'b':{}}},'a.b.c.d', infill=True)
    ({'a': {'b': {'c': {}}}}, {}, 'd')
    >>> find_json_field(None, 'a.b.c.d')
    Traceback (most recent call last):
        ...
    KeyError: 'a'
    >>> find_json_field(None,'a.b.c.d', infill=True)
    ({'a': {'b': {'c': {}}}}, {}, 'd')

## Function `get_json_field(column_value, field_name, *, default=None)`

Return the value of `field_name` from `column_value`
or a defaault if the field is not present.

Parameters:
* `column_value`: the original value of the column
* `field_name`: the field within the column to locate
* `default`: default value to return if the field is not present,
  default: `None`

Examples:

    >>> get_json_field({'a': 1}, 'a')
    1
    >>> get_json_field({'b': 1}, 'a')
    >>> get_json_field({'a': {}}, 'a.b')
    >>> get_json_field({'a': {'b': 2}}, 'a.b')
    2

## Class `ORM`

A convenience base class for an ORM class.

This defines a `.Base` attribute which is a new `DeclarativeBase`
and provides various Session related convenience methods.

Subclasses must define their own `.Session` factory in
their own `__init__`, for example:

    self.Session = sessionmaker(bind=engine)

## Function `orm_auto_session(method)`

Decorator to run a method in a session derived from `self.orm`
if a session is not presupplied.
Intended to assist classes with a `.orm` attribute.

## Function `set_json_field(column_value, field_name, value, *, infill=False)`

Set a new `value` for `field_name` of `column_value`.
Return the new `column_value`.

Parameters:
* `column_value`: the original value of the column
* `field_name`: the field within the column to locate
* `value`: the value to store as `field_name`
* `infill`: optional keyword parameter, default `False`.
  If true,
  `column_value` and its innards will be filled in as `dict`s
  to allow deferencing the `field_name`.

As with `find_json_field`,
a true `infill` may modify `column_value` to provide `field_name`
which is why this function returns the new `column_value`.

Examples:

    >>> set_json_field({'a': 2}, 'a', 3)
    {'a': 3}
    >>> set_json_field({'a': 2, 'b': {'c': 5}}, 'b.c', 4)
    {'a': 2, 'b': {'c': 4}}
    >>> set_json_field({'a': 2}, 'b.c', 4)
    Traceback (most recent call last):
        ...
    KeyError: 'b'
    >>> set_json_field({'a': 2}, 'b.c', 4, infill=True)
    {'a': 2, 'b': {'c': 4}}
    >>> set_json_field(None, 'b.c', 4, infill=True)
    {'b': {'c': 4}}

## Function `with_session(func, *a, orm=None, session=None, **kw)`

Call `func(*a,session=session,**kw)`, creating a session if required.

This is the inner mechanism of `@auto_session` and
`ORM.auto_session_method`.

Parameters:
* `func`: the function to call
* `a`: the positional parameters
* `orm`: optional ORM class with a `.session()` context manager method
* `session`: optional existing ORM session

One of `orm` or `session` must be not `None`; if `session`
is `None` then one is made from `orm.session()` and used as
a context manager. The `session` is also passed to `func` as
the keyword parameter `session` to support nested calls.
