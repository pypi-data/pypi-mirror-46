# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['git_hooks_1c']

package_data = \
{'': ['*']}

install_requires = \
['cjk-commons>=3.3,<4.0', 'fleep>=1.0,<2.0', 'parse-1c-build>=5.5,<6.0']

entry_points = \
{'console_scripts': ['gh1c = git_hooks_1c.__main__:run']}

setup_kwargs = {
    'name': 'git-hooks-1c',
    'version': '9.1.2',
    'description': 'Git hooks utilities for 1C:Enterprise',
    'long_description': '',
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'url': 'https://github.com/Cujoko/git-hooks-1c',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
