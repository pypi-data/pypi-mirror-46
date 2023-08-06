# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['corpy',
 'corpy.morphodita',
 'corpy.phonetics',
 'corpy.scripts',
 'corpy.util',
 'corpy.vertical',
 'corpy.vis']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'lazy>=1.4,<2.0',
 'lxml>=4.3,<5.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.16,<2.0',
 'regex>=2019.4,<2020.0',
 'ufal.morphodita>=1.9,<2.0',
 'wordcloud>=1.5,<2.0']

entry_points = \
{'console_scripts': ['xc = corpy.scripts.xc:main',
                     'zip-verticals = corpy.scripts.zip_verticals:main']}

setup_kwargs = {
    'name': 'corpy',
    'version': '0.1.1',
    'description': 'Tools for processing language data.',
    'long_description': None,
    'author': 'David Lukes',
    'author_email': 'dafydd.lukes@gmail.com',
    'url': 'https://github.com/dlukes/corpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
