# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['libhockey']

package_data = \
{'': ['*']}

install_requires = \
['deserialize==0.9.0', 'requests==2.21.0']

setup_kwargs = {
    'name': 'libhockey',
    'version': '0.5.0',
    'description': 'A Python wrapper around the Hockey App API.',
    'long_description': '\n# Contributing\n\nThis project welcomes contributions and suggestions.  Most contributions require you to agree to a\nContributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us\nthe rights to use your contribution. For details, visit https://cla.microsoft.com.\n\nWhen you submit a pull request, a CLA-bot will automatically determine whether you need to provide\na CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions\nprovided by the bot. You will only need to do this once across all repos using our CLA.\n\nThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).\nFor more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or\ncontact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.\n',
    'author': 'Dale Myers',
    'author_email': 'dalemy@microsoft.com',
    'url': 'https://github.com/Microsoft/libhockey',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
