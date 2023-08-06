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
    'version': '0.1.2',
    'description': 'Tools for processing language data.',
    'long_description': '=====\nCorPy\n=====\n\nWhat is CorPy?\n==============\n\nA fancy plural for *corpus* ;) Also, a collection of handy but not especially\nmutually integrated tools for dealing with linguistic data. It abstracts away\nfunctionality which is often needed in practice in day to day work at the\n`Czech National Corpus <https://korpus.cz>`__, without aspiring to be a fully\nfeatured or consistent NLP framework.\n\nCurrently available sub-packages are:\n\n- `morphodita <corpy/morphodita/README.rst>`__: tokenizing and tagging raw\n  textual data using `MorphoDiTa <https://github.com/ufal/morphodita>`__\n- `vertical <corpy/vertical/README.rst>`__: parsing corpora in the vertical\n  format devised originally for `CWB <http://cwb.sourceforge.net/>`__, used also\n  by `(No)SketchEngine <https://nlp.fi.muni.cz/trac/noske/>`__\n- `phonetics <corpy/phonetics/README.rst>`__: rule-based phonetic transcription\n  of Czech\n\nInstallation\n============\n\n.. code:: bash\n\n   $ pip3 install corpy\n\nRequirements\n============\n\nOnly recent versions of Python 3 are supported by design.\n\nLicense\n=======\n\nCopyright \xc2\xa9 2016--present `\xc3\x9a\xc4\x8cNK <http://korpus.cz>`__/David Luke\xc5\xa1\n\nDistributed under the `GNU General Public License v3\n<http://www.gnu.org/licenses/gpl-3.0.en.html>`__.\n',
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
