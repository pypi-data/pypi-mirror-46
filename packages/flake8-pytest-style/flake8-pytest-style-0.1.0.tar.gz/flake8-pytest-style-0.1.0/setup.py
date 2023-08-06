# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_pytest_style']

package_data = \
{'': ['*']}

install_requires = \
['flake8-plugin-utils>=1.0,<2.0']

entry_points = \
{'flake8.extension': ['PT = flake8_pytest_style.plugin:PytestStylePlugin']}

setup_kwargs = {
    'name': 'flake8-pytest-style',
    'version': '0.1.0',
    'description': '',
    'long_description': "# flake8-pytest-style\n\n[![pypi](https://badge.fury.io/py/flake8-pytest-style.svg)](https://pypi.org/project/flake8-pytest-style)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-pytest-style)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-pytest-style.svg)](https://pypistats.org/packages/flake8-pytest-style)\n[![Build Status](https://travis-ci.com/m-burst/flake8-pytest-style.svg?branch=master)](https://travis-ci.com/m-burst/flake8-pytest-style)\n[![Code coverage](https://codecov.io/gh/m-burst/flake8-pytest-style/branch/master/graph/badge.svg)](https://codecov.io/gh/m-burst/flake8-pytest-style)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nA `flake8` plugin checking common style issues or inconsistencies with `pytest`-based tests.\n\nCurrently the following errors are reported:\n\n* `PT001 use @pytest.fixture() over @pytest.fixture`\n\n* `PT002 configuration for fixture '{name}' specified via positional args, use kwargs`  \ne.g. `@pytest.fixture(scope='module')` is OK, and `@pytest.fixture('module')` is an error\n\n* `PT003 scope='function' is implied in @pytest.fixture()`  \ne.g. `@pytest.fixture(scope='function')` should be replaced with `@pytest.fixture()` \n \n* `PT004 fixture '{name}' does not return anything, add leading underscore`\n \n* `PT005 fixture '{name}' returns a value, remove leading underscore`\n \n* `PT006 wrong name(s) type in @pytest.mark.parametrize, expected {expected_type}`  \ne.g. `@pytest.mark.parametrize(('name1', 'name2'), ...)` is ok,\nand `@pytest.mark.parametrize('name1,name2', ...)` is an error\n \n* `PT007 wrong values type in @pytest.mark.parametrize, expected {expected_type}`\n \n* `PT008 use return_value= instead of patching with lambda`  \ne.g. `mocker.patch('target', return_value=7)` is OK, \nand `mocker.patch('target', lambda *args: 7)` is an error\n\n## Installation\n\n    pip install flake8-pytest-style\n\n## For developers\n\n### Install deps and setup pre-commit hook\n\n    make init\n\n### Run linters, autoformat, tests etc.\n\n    make format lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## License\n\nMIT\n\n## Change Log\n\n### 0.1.0 - 2019-05-23\n\n* initial\n",
    'author': 'Mikhail Burshteyn',
    'author_email': 'mdburshteyn@gmail.com',
    'url': 'https://pypi.org/project/flake8-pytest-style',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
