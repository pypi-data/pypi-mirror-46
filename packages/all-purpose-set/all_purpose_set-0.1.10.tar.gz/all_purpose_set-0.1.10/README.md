# All Purpose Set

*Note: This document is best viewed [on github](https://github.com/olsonpm/py_all-purpose-set).
Pypi's headers are all caps which presents inaccurate information*


<br>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [What is it?](#what-is-it)
- [Why create it?](#why-create-it)
- [Simple usage](#simple-usage)
- [See also](#see-also)
- [Api](#api)
- [Test](#test)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<br>

### What is it?

- A set which doesn't require hashable contents

<br>

### Why create it?

- I often have a need to store non-hashable contents in a set.  For example
  storing a dict isn't possible with the builtin set.

  ```py
  # doesn't work
  someDict = { "key": "value" }
  someSet = { someDict }
  ```

<br>

### Simple usage

```py
from all_purpose_set import ApSet

someDict = { "key": "value" }
someSet = ApSet([someDict])

print(someDict in someSet) # prints True
```

<br>

### See also

- [All Purpose Dict](https://github.com/olsonpm/py_all-purpose-dict)

<br>

### Api

*Note: This api is young and subject to change quite a bit.  There also may be
functionality present in the builtin set which this set doesn't cover.  I'm
willing to add it so please just raise a github issue or PR with details.*

#### class ApSet([a list])
- all methods return `self` unless specified otherwise
- iterates in the order of insertion
- currently the internal methods implemented are
  - \_\_contains\_\_
  - \_\_iter\_\_
  - \_\_len\_\_

##### add(something)

##### clear()

##### has(something) => bool
- a function alternative to `key in aSet`

##### remove(something)
- raises a `KeyError` if the element doesn't exist

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
