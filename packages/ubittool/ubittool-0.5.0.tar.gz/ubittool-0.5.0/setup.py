# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ubittool']

package_data = \
{'': ['*']}

install_requires = \
['IntelHex>=2.2.1,<3.0.0',
 'click>=7.0,<8.0',
 'pyocd==0.19.0',
 'uflash>=1.1.0,<1.2.1']

entry_points = \
{'console_scripts': ['ubit = ubittool.__main__:main']}

setup_kwargs = {
    'name': 'ubittool',
    'version': '0.5.0',
    'description': 'Tool to interface with the BBC micro:bit.',
    'long_description': '# uBitTool\n\n[![codecov](https://codecov.io/gh/carlosperate/ubittool/branch/master/graph/badge.svg)](https://codecov.io/gh/carlosperate/ubittool)\n[![AppVeyor build status](https://ci.appveyor.com/api/projects/status/byfv99vlf6rinxne?svg=true)](https://ci.appveyor.com/project/carlosperate/ubitextract)\n[![Travis build Status](https://travis-ci.org/carlosperate/ubittool.svg?branch=master)](https://travis-ci.org/carlosperate/ubittool)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nUtility to extract a MicroPython program and/or interpreter from a microbit.\n\nInstall in a Python 2.7 virtual environment:\n\n```\npip install .\n```\n\nAlthough pipenv is recommended:\n\n```\npip install pipenv\npipenv install .\n```\n\nTo run:\n\n```\nubit read-code -f extracted_script.py\n```\n\nTo run the GUI:\n\n```\nubit gui\n```\n\nor from this directory:\n\n```\npython -m ubittool gui\n```\n\nTo run the tests, from this directory execute:\n\n```\npython make.py check\n```\n\nTo see what other make actions there are run:\n\n```\npython make.py --help\n```\n',
    'author': 'Carlos Pereira Atencio',
    'author_email': 'carlosperate@embeddedlog.com',
    'url': 'https://carlosperate.github.io/ubittool/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
