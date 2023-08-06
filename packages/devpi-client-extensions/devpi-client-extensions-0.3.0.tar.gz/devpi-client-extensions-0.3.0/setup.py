# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['devpi_ext']

package_data = \
{'': ['*']}

install_requires = \
['devpi-client>=3.0.0']

extras_require = \
{'keyring': ['keyring'], 'keyring:python_version >= "3.5"': ['jeepney']}

entry_points = \
{'devpi_client': ['devpi-client-ext-login-keyring = '
                  'devpi_ext.login:_keyring_plugin [keyring]',
                  'devpi-client-ext-login-pypirc = '
                  'devpi_ext.login:_pypirc_plugin']}

setup_kwargs = {
    'name': 'devpi-client-extensions',
    'version': '0.3.0',
    'description': 'devpi client extensions',
    'long_description': "devpi-client-extensions\n=======================\n\nSome useful stuff around `devpi client`_. Although this package is proudly named *extensions*,\ncurrently there is only one thing implemented ready to be used: a hook that uses passwords from\n``.pypirc`` or `keyring`_ on login to devpi server so you don't have to enter your password\nif you store it for upload anyway.\n\nInstall\n-------\n\n.. code-block:: sh\n\n   $ pip install devpi-client-extensions\n\nUsage\n-----\n\nJust use the ``devpi login`` command as usual:\n\n.. code-block:: sh\n\n   $ devpi login hoefling\n   Using hoefling credentials from .pypirc\n   logged in 'hoefling', credentials valid for 10.00 hours\n\nKeyring Support\n---------------\n\nSince version 0.3, reading credentials using `keyring`_ is supported. Install the package with `keyring` extras:\n\n.. code-block:: sh\n\n   $ pip install devpi-client-extensions[keyring]\n\nExample with storing the password in keyring:\n\n.. code-block:: sh\n\n   $ keyring set https://my.devpi.url/ hoefling\n   $ devpi login hoefling\n   Using hoefling credentials from keyring\n   logged in 'hoefling', credentials valid for 10.00 hours\n\nStats\n-----\n\n|pypi| |build| |appveyor| |coverage| |landscape| |requirements| |black|\n\n.. |pypi| image:: https://badge.fury.io/py/devpi-client-extensions.svg\n   :target: https://badge.fury.io/py/devpi-client-extensions\n   :alt: Package on PyPI\n\n.. |build| image:: https://travis-ci.org/hoefling/devpi-client-extensions.svg?branch=master\n   :target: https://travis-ci.org/hoefling/devpi-client-extensions\n   :alt: Build status\n\n.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/hoefling/devpi-client-extensions?branch=master&svg=true\n   :target: https://ci.appveyor.com/project/hoefling/devpi-client-extensions\n   :alt: Windows build status\n\n.. |coverage| image:: https://codecov.io/gh/hoefling/devpi-client-extensions/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/hoefling/devpi-client-extensions\n   :alt: Coverage status\n\n.. |landscape| image:: https://landscape.io/github/hoefling/devpi-client-extensions/master/landscape.svg?style=flat\n   :target: https://landscape.io/github/hoefling/devpi-client-extensions/master\n   :alt: Code Health\n\n.. |requirements| image:: https://requires.io/github/hoefling/devpi-client-extensions/requirements.svg?branch=master\n     :target: https://requires.io/github/hoefling/devpi-client-extensions/requirements/?branch=master\n     :alt: Requirements status\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. _devpi client: https://pypi.org/project/devpi-client/\n\n.. _keyring: https://pypi.org/project/keyring/\n",
    'author': 'Oleg Höfling',
    'author_email': 'oleg.hoefling@gmail.com',
    'url': 'https://github.com/hoefling/devpi-client-extensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
