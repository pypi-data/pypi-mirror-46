# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cvgen']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'email-validator>=1.0,<2.0',
 'jinja2>=2.10,<3.0',
 'pydantic>=0.25.0,<0.26.0',
 'pyyaml>=5.1,<6.0',
 'weasyprint>=47.0,<48.0']

entry_points = \
{'console_scripts': ['cvgen = cvgen.main:main']}

setup_kwargs = {
    'name': 'cvgen',
    'version': '0.1.3',
    'description': 'A tool for easily creating a good-looking CV in PDF format from .yaml data, HTML & CSS.',
    'long_description': None,
    'author': 'Vadim Galaktionov',
    'author_email': 'vadim@galaktionov.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
