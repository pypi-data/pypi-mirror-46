# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['indextools', 'indextools.console']

package_data = \
{'': ['*']}

install_requires = \
['autoclick>=0.5.1,<0.6.0',
 'ngsindex>=0.1.7,<0.2.0',
 'pysam>=0.15,<0.16',
 'xphyle>=4.0.8,<5.0.0']

entry_points = \
{'console_scripts': ['indextools = indextools.console:indextools']}

setup_kwargs = {
    'name': 'indextools',
    'version': '0.1.1',
    'description': 'A toolkit for accelerating genomics using index files. ',
    'long_description': None,
    'author': 'John Didion',
    'author_email': 'jdidion@dnanexus.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
