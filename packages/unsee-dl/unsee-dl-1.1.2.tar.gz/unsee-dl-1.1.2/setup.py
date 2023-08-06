# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['unsee']

package_data = \
{'': ['*']}

modules = \
['unsee_dl']
install_requires = \
['websockets>=7.0,<8.0']

entry_points = \
{'console_scripts': ['unsee-dl = unsee_dl:main']}

setup_kwargs = {
    'name': 'unsee-dl',
    'version': '1.1.2',
    'description': 'unsee.cc downloader',
    'long_description': '# [unsee.cc](https://unsee.cc) downloader\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![PyPI](https://img.shields.io/pypi/v/unsee-dl.svg)](https://pypi.org/project/unsee-dl/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unsee-dl.svg)](https://pypi.org/project/unsee-dl/)\n\n# Usage\n\n```\npip install unsee-dl\n\nunsee-dl [-o OUT_DIR] <id...>\n```\n',
    'author': 'Andrea Salamone',
    'author_email': 'andrea.sala96@gmail.com',
    'url': 'https://github.com/andsala/unsee-dl',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
