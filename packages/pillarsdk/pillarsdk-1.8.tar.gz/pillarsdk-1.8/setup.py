# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pillarsdk']

package_data = \
{'': ['*']}

install_requires = \
['pyOpenSSL==16.2.0', 'requests==2.13.0']

setup_kwargs = {
    'name': 'pillarsdk',
    'version': '1.8',
    'description': 'The Pillar REST SDK provides Python APIs to communicate to the Pillar webservices.',
    'long_description': None,
    'author': 'Francesco Siddi',
    'author_email': 'francesco@blender.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
