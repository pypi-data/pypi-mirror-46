# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_plugin_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flake8-plugin-utils',
    'version': '1.0.0',
    'description': 'The package provides base classes and utils for flake8 plugin writing',
    'long_description': "# flake8-plugin-utils\n\n[![pypi](https://badge.fury.io/py/flake8-plugin-utils.svg)](https://pypi.org/project/flake8-plugin-utils)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-plugin-utils)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-plugin-utils.svg)](https://pypistats.org/packages/flake8-plugin-utils)\n[![Build Status](https://travis-ci.org/Afonasev/flake8-plugin-utils.svg?branch=master)](https://travis-ci.org/Afonasev/flake8-plugin-utils)\n[![Code coverage](https://codecov.io/gh/afonasev/flake8-plugin-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/afonasev/flake8-plugin-utils)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nThe package provides base classes and utils for flake8 plugin writing.\n\n## Installation\n\n```bash\npip install flake8-plugin-utils\n```\n\n## Example\n\nWrite simple plugin\n\n```python\nfrom flake8_plugin_utils import Error, Visitor, Plugin\n\nclass MyError(Error):\n    code = 'X100'\n    message = 'my error'\n\nclass MyVisitor(Visitor):\n    def visit_ClassDef(self, node):\n        self.error_from_node(MyError, node)\n\nclass MyPlugin(Plugin):\n    name = 'MyPlugin'\n    version = '0.1.0'\n    visitors = [MyVisitor]\n```\n\nand test it with pytest\n\n```python\nfrom flake8_plugin_utils import assert_error, assert_not_error\n\ndef test_code_with_error():\n    assert_error(MyVisitor, 'class Y: pass', MyError)\n\ndef test_code_without_error():\n    assert_not_error(MyVisitor, 'x = 1')\n```\n\n### Formatting\n\nYour `Error`s can take formatting arguments in their `message`:\n\n```python\nfrom flake8_plugin_utils import Error, Visitor, assert_error\n\nclass MyFormattedError(Error):\n    code = 'X101'\n    message = 'my error with {thing}'\n\nclass MyFormattedVisitor(Visitor):\n    def visit_ClassDef(self, node):\n        self.error_from_node(MyFormattedError, node, thing=node.name)\n\ndef test_code_with_error():\n    assert_error(\n        MyFormattedVisitor,\n        'class Y: pass',\n        MyFormattedError,\n        thing='Y',\n    )\n```\n\n## License\n\nMIT\n\n## Change Log\n\nUnreleased\n-----\n\n* ...\n\n1.0.0 - 2019-05-23\n-----\n\n* add message formatting to Error\n\n0.2.1 - 2019-04-01\n-----\n\n* don`t strip before src dedent in _error_from_src\n* add is_none, is_true, is_false util functions\n\n0.2.0 - 2019.02.21\n-----\n\n* add assert methods\n\n0.1.0 - 2019.02.09\n-----\n\n* initial\n",
    'author': 'Afonasev Evgeniy',
    'author_email': 'ea.afonasev@gmail.com',
    'url': 'https://pypi.org/project/flake8-plugin-utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
