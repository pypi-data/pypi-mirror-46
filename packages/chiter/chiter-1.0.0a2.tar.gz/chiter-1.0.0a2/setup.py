# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chiter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chiter',
    'version': '1.0.0a2',
    'description': 'iterable as a chain',
    'long_description': '# ChIter - iterable as a chain\n\n## Requirements\n* Python 3.7+\n\n## Installation\n```bash\npip install chiter\n```\n\n## Documentation\nComing soon\n\n## Why?\n* Chains do not require saving the intermediate state in temporary variables\n* Look more readable\n\n### Examples\nIt is necessary to get the sum of all numbers from the following sequence:`"23,45,67\\n45,56,55\\n\\n45,a,5\\n-45,56,0"`\n\n#### first way\n```python\nfrom itertools import chain\n\n\ndata = "23,45,67\\n45,56,55\\n\\n45,a,5\\n-45,56,0"\n\nchunks = (chunk.split(\',\') for chunk in data.split())\nflat_data = chain.from_iterable(chunks)\nitems = (int(item) for item in flat_data if not item.isalpha())\nresult = sum(items)\n\nassert result == 352\n```\n#### second way\n```python\nfrom itertools import chain\n\n\ndata = "23,45,67\\n45,56,55\\n\\n45,a,5\\n-45,56,0"\n\nresult = sum((\n    int(item)\n    for item in chain.from_iterable(map(lambda c: c.split(\',\'), data.split()))\n    if not item.isalpha()\n))\nassert result == 352\n```\n#### chiter way\n```python\nfrom chiter import ChIter as I\n\n\ndata = "23,45,67\\n45,56,55\\n\\n45,a,5\\n-45,56,0"\n\nresult = (I(data.split())\n          .map(lambda x: x.split(\',\'))\n          .flat()\n          .filterfalse(str.isalpha)\n          .map(int)\n          .sum())\n\nassert result == 352\n```\n\n## Related Libraries\n* [flupy](https://github.com/olirice/flupy)',
    'author': 'Yaroslav Bibaev',
    'author_email': 'yaroslav@gmx.com',
    'url': 'https://github.com/nede1/chiter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
