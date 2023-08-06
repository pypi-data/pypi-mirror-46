# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['projmap']

package_data = \
{'': ['*'], 'projmap': ['data/*']}

install_requires = \
['cartopy>=0.17.0,<0.18.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'scipy>=1.3,<2.0',
 'six>=1.12,<2.0']

setup_kwargs = {
    'name': 'projmap',
    'version': '0.8.5',
    'description': 'High level wrapper of matplotlibs mapping package',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
