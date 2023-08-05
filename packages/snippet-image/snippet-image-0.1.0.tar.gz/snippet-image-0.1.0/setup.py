# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snippet_image']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=6.0,<7.0']

setup_kwargs = {
    'name': 'snippet-image',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'acrius',
    'author_email': 'acrius@mail.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
