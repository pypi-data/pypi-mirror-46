# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['selenium_probes', 'selenium_probes.helpers', 'selenium_probes.probes']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141,<4.0']

extras_require = \
{'code-format': ['black>=19.3b0,<20.0', 'blacken-docs>=0.5.0,<0.6.0'],
 'code-lint': ['flake8>=3.7,<4.0',
               'flake8-import-order>=0.18.1,<0.19.0',
               'flake8-bandit>=2.1,<3.0',
               'flake8-blind-except>=0.1.1,<0.2.0',
               'flake8-bugbear>=19.3,<20.0',
               'flake8-builtins>=1.4,<2.0',
               'flake8-docstrings>=1.3,<2.0',
               'flake8-logging-format>=0.6.0,<0.7.0',
               'pep8-naming>=0.8.2,<0.9.0',
               'pygments>=2.4,<3.0'],
 'docs': ['recommonmark>=0.5.0,<0.6.0',
          'sphinx>=2.0,<3.0',
          'sphinx_rtd_theme>=0.4.3,<0.5.0'],
 'keyvault': ['azure-keyvault>=1.1,<2.0'],
 'test': ['pytest>=4.4.2,<5.0.0',
          'pytest-cov>=2.7,<3.0',
          'pytest-dockerc>=1.0,<2.0',
          'pytest-instafail>=0.4.1,<0.5.0',
          'pytest-lazy-fixture>=0.5.2,<0.6.0',
          'pytest-random-order>=1.0,<2.0',
          'pytest-variables[yaml]>=1.7,<2.0']}

setup_kwargs = {
    'name': 'selenium-probes',
    'version': '0.1.0',
    'description': 'A framework for building Selenium-based probes.',
    'long_description': '# SeleniumProbes\n\n ![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][BlackRef] [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)][MITRef]\n\n[BlackRef]: https://github.com/ambv/black\n[MITRef]: https://opensource.org/licenses/MIT\n\n`SeleniumProbes` is a library of building blocks to construct probes generating metrics for automated testing of web app performance and availability like accessing a login page, authenticating on it and then triggering some functionality by clicking on a web element.\n\n## Getting Started\n\nFollow these instructions to use the package in your project.\n\n### Installing\n\n`SeleniumProbes` library could be added to your project by installing it from the Python Package Index (PyPI) repository. Run the following command to:\n\n* install a specific version\n\n    ```sh\n    pip install "selenium_probes==0.1"\n    ```\n\n* install the latest version\n\n    ```sh\n    pip install "selenium_probes"\n    ```\n\n* upgrade to the latest version\n\n    ```sh\n    pip install --upgrade "selenium_probes"\n    ```\n\n* install optional dependencies like Microsoft Azure libraries to use KeyVault helper to work (not everybody would need that, hence it is an optional dependency)\n\n    ```sh\n    pip install "selenium_probes[keyvault]"\n    ```\n\n### Requirements\n\nPyPI packages:\n\n* Python >= 3.6\n* [selenium >= 3.141.0][SeWebDriverRef]\n\n\n[SeWebDriverRef]: https://pypi.org/project/selenium/\n\n### Deployment\n\nThis library package is not intended for stand-alone deployment. It should be used as part of some webapp-specific probe. See [SeleniumBottle][SeleniumBottleProjectRef] project as an example.\n\n[SeleniumBottleProjectRef]: https://github.com/undp/SeleniumBottle\n\n## Built using\n\n* [Selenium WebDriver][SeWebDriverRef] - Web browser interactions\n\n## Versioning\n\nWe use [Semantic Versioning Specification][SemVer] as a version numbering convention.\n\n[SemVer]: http://semver.org/\n\n## Release History\n\nFor the available versions, see the [tags on this repository][RepoTags]. Specific changes for each version are documented in [CHANGES.md][ChangelogRef].\n\nAlso, conventions for `git commit` messages are documented in [CONTRIBUTING.md][ContribRef].\n\n[RepoTags]: https://github.com/undp/SeleniumProbes/tags\n[ChangelogRef]: CHANGES.md\n[ContribRef]: CONTRIBUTING.md\n\n## Authors\n\n* **Oleksiy Kuzmenko** - [OK-UNDP@GitHub][OK-UNDP@GitHub] - *Initial work*\n\n[OK-UNDP@GitHub]: https://github.com/OK-UNDP\n\n## Acknowledgments\n\n* Hat tip to anyone helping.\n\n## License\n\nUnless otherwise stated, all authors (see commit logs) release their work under the [MIT License][MITRef]. See [LICENSE.md][LicenseRef] for details.\n\n[LicenseRef]: LICENSE.md\n\n## Contributing\n\nThere are plenty of ways you could contribute to this project. Feel free to:\n\n* submit bug reports and feature requests\n* outline, fix and expand documentation\n* peer-review bug reports and pull requests\n* implement new features or fix bugs\n\nSee [CONTRIBUTING.md][ContribRef] for details on code formatting, linting and testing frameworks used by this project.\n',
    'author': 'Oleksiy Kuzmenko',
    'author_email': 'oleksiy.kuzmenko@undp.org',
    'url': 'https://github.com/undp/SeleniumProbes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
