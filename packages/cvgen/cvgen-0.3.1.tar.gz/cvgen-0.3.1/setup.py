# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cvgen']

package_data = \
{'': ['*'],
 'cvgen': ['templates/index.html.j2',
           'templates/index.html.j2',
           'templates/style.css',
           'templates/style.css']}

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
    'version': '0.3.1',
    'description': 'A tool for easily creating a good-looking CV in PDF format from .yaml data, HTML & CSS.',
    'long_description': '# CVgen\n\n> A tool for easily creating a good-looking CV in PDF format from .yaml data, HTML & CSS.\n\nBuilt with:\n\n- Python 3\n- Jinja2\n- WeasyPrint\n- PyYAML\n- Pydantic\n- Click\n- Poetry\n\n## Install\n\n```bash\npip install cvgen\n```\n\n## Usage\n\nCVgen expects an input YAML file in this format:\n\n```yaml\n---\nname: Mr Job Man\n\npersonalia:\n  phone: +31 6 1234 5678\n  address: Noordeinde 68, 2514 GL Den Haag\n  email: mr.job.man@gmail.com\n  nationality: Dutch\n\nexperience:\n  - title: Widget Engineer @ Widget Inc\n    industry: widget manufacturing\n    dates: April 2007 - present\n    description: >-\n      Various widget manufacturing tasks.\n\neducation:\n  - diploma: MSc Widget Management\n    institution: University of Widgetry\n    dates: 2006 - 2007\n    description: >-\n      Various widget management topics.\n\nskills:\n  - category: Computer\n    keywords:\n      - Ctrl + Alt + Delete\n      - Minesweeper\n      - Lotus Notes\n\nprojects:\n  - title: DIY widget 3D printer\n    description: >-\n      Made a 3D printer for widgets\n\nactivities:\n  - title: Cricket player\n    organization: Cricket club\n    dates: 2015 - 2016\n    description: >-\n      Whatever cricket players do\n```\n\nRun it like:\n\n```bash\ncvgen [input_file]\n```\n\n## Contributing\n\nPRs accepted for additional templates/styles/features.\n\n## License\n\nMIT © Vadim Galaktionov\n',
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
