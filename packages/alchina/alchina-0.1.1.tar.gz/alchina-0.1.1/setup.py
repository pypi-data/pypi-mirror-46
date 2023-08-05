# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['alchina']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'scikit-learn>=0.20.3,<0.21.0']

setup_kwargs = {
    'name': 'alchina',
    'version': '0.1.1',
    'description': 'Machine Learning framework',
    'long_description': '# Alchina /al.ki.na/\n\n[![Build Status](https://travis-ci.org/matthieugouel/alchina.svg?branch=master)](https://travis-ci.org/matthieugouel/alchina)\n[![Coverage Status](https://coveralls.io/repos/github/matthieugouel/alchina/badge.svg?branch=master)](https://coveralls.io/github/matthieugouel/alchina?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![license](https://img.shields.io/github/license/matthieugouel/gibica.svg)](https://github.com/matthieugouel/gibica/blob/master/LICENSE)\n\nAlchina is a Machine Learning framework.\n',
    'author': 'matthieu',
    'author_email': 'matthieu.gouel@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
