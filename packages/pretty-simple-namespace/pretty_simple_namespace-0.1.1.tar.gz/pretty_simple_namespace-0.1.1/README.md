# Pretty SimpleNamespace

*Note: This document is best viewed [on github](https://github.com/olsonpm/py_pretty-simple-namespace).
Pypi's headers are all caps which presents inaccurate information*


<br>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [What is it?](#what-is-it)
- [Why create it?](#why-create-it)
- [Simple usage](#simple-usage)
- [Features](#features)
- [Limitations](#limitations)
- [Related projects](#related-projects)
- [Api](#api)
- [Test](#test)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<br>

### What is it?

- A stringifier and formatter for SimpleNamespace which attempts to make the
  data as readable as possible.

<br>

### Why create it?

- I use SimpleNamespace often to hold state and needed a way to print it out for
  debugging purposes.

<br>

### Simple usage

```py
from pretty_simple_namespace import pprint
from types import SimpleNamespace as o

joe = o(
    name={"first": "joe", "last": "schmo"},
    age=30,
    favoriteFoods=["apples", "steak"],
)

pprint(joe)
# prints
# {
#   name: {
#     first: 'joe'
#     last: 'schmo'
#   }
#   age: 30
#   favoriteFoods: [
#     'apples'
#     'steak'
#   ]
# }
```

<br>

### Features
- handles recursive structures by tracking and printing references nicely
- recurses into types `list`, `dict` and `SimpleNamespace` for now
- has special-case printing for types `bool`, `str`, `callable` and `None`
  - booleans and None are printed lowercase
  - strings are wrapped in single quotes
  - callable appends `()` e.g. `myMethod()`.  Arguments aren't represented
- all other types are printed by wrapping it in `str` e.g. `str(userDefinedType)`

<br>

### Limitations
- multi-line strings look ugly
- doesn't have a way to recurse into structures other than what's listed above

<br>

### Related projects

- [tedent](https://github.com/olsonpm/py_tedent)

<br>

### Api

#### format(something, indent=2) => str
- formats `something` to a string as seen in [Simple usage](#simple-usage)

#### pprint(something, indent=2) => None
- just prints the formated `something`

#### wrapWith(\*, indent) => [Wrapped module](#wrapped-module)
- use this when you want to call `format` or `pprint` with a different default
  indent value so you don't have to pass it manually all the time.

  e.g.
  ```py
  from pretty_simple_namespace import wrapWith

  pprint = wrapWith(indent=4).pprint
  pprint(o(tabbed4spaces=True))
  # {
  #     tabbed4spaces: true
  # }
  ```

#### Wrapped module
- just an instance of SimpleNamespace with two attributes `format` and `pprint`.

<br>

### Test

```sh
#
# you must have poetry installed
#
$ poetry shell
$ poetry install
$ python runTests.py
```
