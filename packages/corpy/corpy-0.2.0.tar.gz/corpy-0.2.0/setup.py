# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['corpy', 'corpy.morphodita', 'corpy.util', 'corpy.vertical', 'corpy.vis']

package_data = \
{'': ['*'], 'corpy': ['phonetics/*', 'scripts/*']}

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
    'version': '0.2.0',
    'description': 'Tools for processing language data.',
    'long_description': "=====\nCorPy\n=====\n\n.. image:: https://readthedocs.org/projects/corpy/badge/?version=latest\n   :target: https://corpy.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation status\n\n.. image:: https://badge.fury.io/py/corpy.svg\n   :target: https://badge.fury.io/py/corpy\n   :alt: PyPI package\n\nWhat is CorPy?\n==============\n\nA fancy plural for *corpus* ;) Also, a collection of handy but not especially\nmutually integrated tools for dealing with linguistic data. It abstracts away\nfunctionality which is often needed in practice for teaching and/or day to day\nwork at the `Czech National Corpus <https://korpus.cz>`__, without aspiring to\nbe a fully featured or consistent NLP framework.\n\nThe short URL to the docs is: https://corpy.rtfd.io/\n\nHere's an idea of what you can do with CorPy:\n\n- `tokenize and morphologically tag\n  <https://corpy.rtfd.io/en/latest/guides/morphodita.html>`__ raw textual data\n  using `MorphoDiTa <https://github.com/ufal/morphodita>`__\n- `easily generate word clouds\n  <https://corpy.rtfd.io/en/latest/guides/vis.html>`__\n- `generate phonetic transcripts of Czech texts\n  <https://corpy.rtfd.io/en/latest/guides/phonetics_cs.html>`__\n- `wrangle corpora in the vertical format\n  <https://corpy.rtfd.io/en/latest/guides/vertical.html>`__ devised originally\n  for `CWB <http://cwb.sourceforge.net/>`__, used also by `(No)SketchEngine\n  <https://nlp.fi.muni.cz/trac/noske/>`__\n- plus some `command line utilities\n  <https://corpy.rtfd.io/en/latest/guides/cli.html>`__\n\nInstallation\n============\n\n.. code:: bash\n\n   $ pip3 install corpy\n\nRequirements\n============\n\nOnly recent versions of Python 3 (3.6+) are supported by design.\n\n.. license-marker\n\nLicense\n=======\n\nCopyright © 2016--present `ÚČNK <http://korpus.cz>`__/David Lukeš\n\nDistributed under the `GNU General Public License v3\n<http://www.gnu.org/licenses/gpl-3.0.en.html>`__.\n",
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
