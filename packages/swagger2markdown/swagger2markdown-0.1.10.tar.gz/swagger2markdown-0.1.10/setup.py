# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['swagger2markdown']
install_requires = \
['Jinja2>=2.10,<3.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['swagger2markdown = swagger2markdown:main']}

setup_kwargs = {
    'name': 'swagger2markdown',
    'version': '0.1.10',
    'description': 'Converter from Swagger JSON to Markdown.',
    'long_description': None,
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
