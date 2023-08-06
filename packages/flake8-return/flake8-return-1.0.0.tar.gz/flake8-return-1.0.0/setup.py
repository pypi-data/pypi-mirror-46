# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_return']

package_data = \
{'': ['*']}

install_requires = \
['flake8-plugin-utils>=0.2.0,<0.3.0']

entry_points = \
{'flake8.extension': ['R50 = flake8_return.plugin:ReturnPlugin']}

setup_kwargs = {
    'name': 'flake8-return',
    'version': '1.0.0',
    'description': 'Flake8 plugin that checks return values',
    'long_description': '# flake8-return\n\n[![pypi](https://badge.fury.io/py/flake8-return.svg)](https://pypi.org/project/flake8-return)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-return)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-return.svg)](https://pypistats.org/packages/flake8-return)\n[![Build Status](https://travis-ci.org/Afonasev/flake8-return.svg?branch=master)](https://travis-ci.org/Afonasev/flake8-return)\n[![Code coverage](https://codecov.io/gh/afonasev/flake8-return/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-return)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nFlake8 plugin that checks return values.\n\n## Installation\n\n```bash\npip install flake8-return\n```\n\n## Errors\n\n* R501 you shouldn\\`t add None at any return if function havn\\`t return value except None\n\n```python\ndef x(y):\n    if not y:\n        return\n    return None  # error!\n```\n\n* R502 you should add explicit value at every return if function have return value except None\n\n```python\ndef x(y):\n    if not y:\n        return  # error!\n    return 1\n```\n\n* R503 you should add explicit return at end of the function if function have return value except None\n\n```python\ndef x(y):\n    if not y:\n        return  # error!\n    return 1\n```\n\n* R504 you shouldn`t assign value to variable if it will be use only as return value\n\n```python\ndef x():\n    a = 1\n    # some code that not using `a`\n    print(\'test\')\n    return a  # error!\n```\n\nReturns in asyncio coroutines also supported.\n\n## License\n\nMIT\n\n## Change Log\n\n### 1.0.0 - 2019-05-13\n\n* skip assign after unpacking while unnecessary assign checking "(x, y = my_obj)"\n\n### 0.3.2 - 2019-04-01\n\n* allow "assert False" as last function return\n\n### 0.3.1 - 2019-03-11\n\n* add pypi deploy into travis config\n* add make bump_version command\n\n### 0.3.0 - 2019-02-26\n\n* skip functions that consist only `return None`\n* fix false positive when last return inner with statement\n* add unnecessary assign error\n* add support tuple in assign or return expressions\n* add suppport asyncio coroutines\n\n### 0.2.0 - 2019-02-21\n\n* fix explicit/implicit\n* add flake8-plugin-utils as dependency\n* allow raise as last function return\n* allow no return as last line in while block\n* fix if/elif/else cases\n\n### 0.1.1 - 2019-02-10\n\n* fix error messages\n\n### 0.1.0 - 2019-02-10\n\n* initial\n',
    'author': 'Afonasev Evgeniy',
    'author_email': 'ea.afonasev@gmail.com',
    'url': 'https://pypi.org/project/flake8-return',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
