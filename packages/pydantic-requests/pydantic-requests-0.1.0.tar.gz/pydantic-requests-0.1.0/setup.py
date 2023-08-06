# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydantic_requests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=0.25.0,<0.26.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'pydantic-requests',
    'version': '0.1.0',
    'description': 'A pydantic integration with requests.',
    'long_description': None,
    'author': 'Janez Troha',
    'author_email': 'dz0ny@ubuntu.si',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
