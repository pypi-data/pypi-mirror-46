# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['buzz']

package_data = \
{'': ['*']}

install_requires = \
['deprecated>=1.2,<2.0', 'inflection>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'py-buzz',
    'version': '1.0.0',
    'description': '"That\'s not flying, it\'s falling with style: Exceptions with extras"',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
