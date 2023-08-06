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
    'version': '1.0.1',
    'description': '"That\'s not flying, it\'s falling with style: Exceptions with extras"',
    'long_description': ".. image::  https://badge.fury.io/py/py-buzz.svg\n   :target: https://badge.fury.io/py/py-buzz\n   :alt:    Latest Version\n\n.. image::  https://travis-ci.org/dusktreader/py-buzz.svg?branch=integration\n   :target: https://travis-ci.org/dusktreader/py-buzz\n   :alt:    Build Status\n\n.. image::  https://readthedocs.org/projects/py-buzz/badge/?version=latest\n   :target: http://py-buzz.readthedocs.io/en/latest/?badge=latest\n   :alt:    Documentation Status\n\n*********\n py-buzz\n*********\n\n------------------------------------------------------------------\nThat's not flying, it's falling with style: Exceptions with extras\n------------------------------------------------------------------\n\nThis package supplies some extras to python exceptions that may be useful\nwithin a python project. It is intended to supply some functionality that is\noften written over and over again in packages. Most of the features are\nrelatively simple, but providing a consistent set of functionality is very\nconvenient when dealing with exceptions within your projects.\n\nBuzz can be used as a stand-alone exception class, but it is best used as a\nbase class for custom exceptions within a package. This allows the user to\nfocus on creating a set of Exceptions that provide complete coverage for issues\nwithin their application without having to re-write convenience functions on\ntheir base Exception class\n\nSuper-quick Start\n-----------------\n - requirements: `python3`\n - install through pip: `$ pip install py-buzz`\n - minimal usage example: `examples/basic.py <https://github.com/dusktreader/py-buzz/tree/master/examples/basic.py>`_\n\nDocumentation\n-------------\n\nThe complete documentation can be found at the\n`py-buzz home page <http://py-buzz.readthedocs.io>`_\n",
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
