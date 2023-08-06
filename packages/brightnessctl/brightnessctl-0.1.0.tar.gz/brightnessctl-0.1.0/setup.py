# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['brightnessctl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['brightnessctl = brightnessctl:main']}

setup_kwargs = {
    'name': 'brightnessctl',
    'version': '0.1.0',
    'description': 'Control screen brightness on Linux',
    'long_description': '# brightnessctl - Control screen brightness on Linux\nInspired by [brightnessctl](https://github.com/Hummer12007/brightnessctl)\n\n\n# Installation\n`pip install --user brightnessctl`\n\n\n# Usage\n```sh\nusage: brightnessctl [-h] [-v] [-p N | -d N | -r N] [--duration S]\n                     [--save | --restore]\n\noptional arguments:\n  -h, --help          show this help message and exit\n  -v, --verbose\n  -p N, --percent N   Set brightness to <N> %\n  -d N, --delta N     Adjust brightness by <N> % of max brightness\n  -r N, --relative N  Adjust brightness by <N> % of current brightness\n  --duration S        How long to take to get to final value\n  --save              Save current value to disk before changing value\n  --restore           Restore saved value from disk\n```\n',
    'author': 'Matt Clement',
    'author_email': 'm@nullroute.host',
    'url': 'https://gitlab.com/mattclement/brightnessctl',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
