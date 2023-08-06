# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['openapi_conformance']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=4.7,<5.0',
 'openapi_core>=0.8,<0.9',
 'toolz>=0.9.0,<0.10.0',
 'validators>=0.12.4,<0.13.0',
 'werkzeug>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'openapi-conformance',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Bradburn',
    'author_email': 'daniel@crunchrapps.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
