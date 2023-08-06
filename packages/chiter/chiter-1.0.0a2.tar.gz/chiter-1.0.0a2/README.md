# ChIter - iterable as a chain

## Requirements
* Python 3.7+

## Installation
```bash
pip install chiter
```

## Documentation
Coming soon

## Why?
* Chains do not require saving the intermediate state in temporary variables
* Look more readable

### Examples
It is necessary to get the sum of all numbers from the following sequence:`"23,45,67\n45,56,55\n\n45,a,5\n-45,56,0"`

#### first way
```python
from itertools import chain


data = "23,45,67\n45,56,55\n\n45,a,5\n-45,56,0"

chunks = (chunk.split(',') for chunk in data.split())
flat_data = chain.from_iterable(chunks)
items = (int(item) for item in flat_data if not item.isalpha())
result = sum(items)

assert result == 352
```
#### second way
```python
from itertools import chain


data = "23,45,67\n45,56,55\n\n45,a,5\n-45,56,0"

result = sum((
    int(item)
    for item in chain.from_iterable(map(lambda c: c.split(','), data.split()))
    if not item.isalpha()
))
assert result == 352
```
#### chiter way
```python
from chiter import ChIter as I


data = "23,45,67\n45,56,55\n\n45,a,5\n-45,56,0"

result = (I(data.split())
          .map(lambda x: x.split(','))
          .flat()
          .filterfalse(str.isalpha)
          .map(int)
          .sum())

assert result == 352
```

## Related Libraries
* [flupy](https://github.com/olirice/flupy)