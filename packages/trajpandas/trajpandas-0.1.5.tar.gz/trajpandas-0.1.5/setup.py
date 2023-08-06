# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['trajpandas', 'trajpandas.io', 'trajpandas.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0', 'pandas>=0.24.2,<0.25.0', 'scipy>=1.2,<2.0']

setup_kwargs = {
    'name': 'trajpandas',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
