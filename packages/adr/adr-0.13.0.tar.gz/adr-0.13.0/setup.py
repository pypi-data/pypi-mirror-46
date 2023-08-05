# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['adr', 'adr.export', 'adr.util', 'app', 'recipes']

package_data = \
{'': ['*'], 'app': ['static/*', 'templates/*'], 'recipes': ['queries/*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'cachy>=0.2.0,<0.3.0',
 'docutils>=0.14,<0.15',
 'flask>=1.0.2,<2.0.0',
 'json-e>=3.0.0,<4.0.0',
 'markdown>=3.0.1,<4.0.0',
 'orderedset>=2.0.1,<3.0.0',
 'pygments>=2.3.1,<3.0.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.21.0,<3.0.0',
 'terminaltables>=3.1.0,<4.0.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['adr = adr.cli:main',
                     'adr-app = app.app:main',
                     'adr-gist = adr.export.gist:cli',
                     'adr-test = adr.export.test:cli']}

setup_kwargs = {
    'name': 'adr',
    'version': '0.13.0',
    'description': 'Utility for running ActiveData recipes',
    'long_description': '[![Build Status](https://travis-ci.org/mozilla/active-data-recipes.svg?branch=master)](https://travis-ci.org/mozilla/active-data-recipes)\n[![PyPI version](https://badge.fury.io/py/active-data-recipes.svg)](https://badge.fury.io/py/active-data-recipes)\n[![PyPI version](https://readthedocs.org/projects/active-data-recipes/badge/?version=latest)](https://active-data-recipes.readthedocs.io)\n\n# active-data-recipes\n\nA repository of various ActiveData recipes. A recipe is a small snippet that runs one or more active\ndata queries and returns the output. Queries can sometimes be modified by command line arguments and\noutput can sometimes be post-processed.\n\nEach recipe should try to answer a single question.\n\n# Software requirements\n\n- You will need Python 3.6 or higher to run the program.\n\n\n# Installation\n\n    pip install active-data-recipes\n\n# Usage\n\nRun:\n\n    adr <recipe> <options>\n\nFor a list of recipes:\n\n    adr --list\n\nFor recipe specific options see:\n\n    adr <recipe> -- --help\n\n# Recipes\n\nSee the [recipe documentation][1] for more information on which recipes are available and how to run\nthem.\n\n# Development\n\nTo contribute to `active-data-recipes` first [install poetry][2], then run:\n\n    git clone https://github.com/mozilla/active-data-recipes\n    cd active-data-recipes\n    poetry install\n\nNow you can use `poetry run` to perform various development commands:\n\n    # run adr\n    poetry run adr <recipe>\n    \n    # run webapp\n    poetry run adr-app\n    \n    # run tests\n    poetry run tox\n\nAlternatively activate the `poetry` shell ahead of time:\n\n    poetry shell\n    \n    # run adr\n    adr <recipe>\n    \n    # run app\n    adr-app\n    \n    # run tests\n    tox\n\n[0]: https://github.com/klahnakoski/ActiveData/blob/dev/docs/jx_time.md\n[1]: https://active-data-recipes.readthedocs.io/en/latest/recipes.html\n[2]: https://poetry.eustace.io/docs/#installation\n',
    'author': 'Andrew Halberstadt',
    'author_email': 'ahalberstadt@mozilla.com',
    'url': 'https://github.com/mozilla/active-data-recipes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
