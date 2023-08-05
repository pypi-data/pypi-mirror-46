# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['docci']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'docci',
    'version': '0.2.0',
    'description': 'Various document utils',
    'long_description': '# docci\n\nVarious document management utils',
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'url': 'https://github.com/potykion/docci',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
