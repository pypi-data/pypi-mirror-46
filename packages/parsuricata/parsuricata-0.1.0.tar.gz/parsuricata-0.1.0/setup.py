# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['parsuricata']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'parsuricata',
    'version': '0.1.0',
    'description': 'Parse Suricata rules',
    'long_description': '# parsuricata\n\nParse Suricata rules\n\n\n# Installation\n\n```bash\npip install parsuricata\n```\n\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
