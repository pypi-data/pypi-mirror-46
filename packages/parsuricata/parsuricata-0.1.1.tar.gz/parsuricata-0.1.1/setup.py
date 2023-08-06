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
    'version': '0.1.1',
    'description': 'Parse Suricata rules',
    'long_description': '# parsuricata\n\nParse Suricata rules\n\n\n# Installation\n\n```bash\npip install parsuricata\n```\n\n\n# Usage\n\n```python\nfrom parsuricata import parse_rules\n\nsource = \'\'\'\n  alert http $HOME_NET any -> !$HOME_NET any (msg: "hi mum!"; content: "heymum"; http_uri; sid: 1;)\n\'\'\'\n\nrules = parse_rules(source)\nprint(rules)\n#\n# alert http $HOME_NET any -> !$HOME_NET any ( \\\n#   msg: hi mum!; \\\n#   content: heymum; \\\n#   http_uri; \\\n#   sid: 1; \\\n# )\n\nrule = rules[0]\n\nprint(rule.action)\n# alert\n\nprint(rule.protocol)\n# http\n\nprint(rule.src)\n# $HOME_NET\n\nprint(rule.src_port)\n# any\n\nprint(rule.direction)\n# ->\n\nprint(rule.dst)\n# !$HOME_NET\n\nprint(rule.dst_port)\n# any\n\nfor option in rule.options:\n    print(f\'{option.keyword} = {option.settings}\')\n#\n# msg = hi mum!\n# content = heymum\n# http_uri = None\n# sid = 1\n```\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
