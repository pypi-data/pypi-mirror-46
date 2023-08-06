# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['noodle']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noodle',
    'version': '0.0.1',
    'description': 'Create beautiful and lightweight Command Lines Tools.',
    'long_description': '# Noodle\n\n[![Build Status](https://travis-ci.org/wilfredinni/noodle.svg?branch=master)](https://travis-ci.org/wilfredinni/noodle) [![codecov](https://codecov.io/gh/wilfredinni/noodle/branch/master/graph/badge.svg)](https://codecov.io/gh/wilfredinni/noodle) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/wilfredinni/mary/blob/master/LICENSE)\n\n\nEasily create beautiful and lightweight Command Line tools\n\n```python\n# cli.py\nimport noodle\n\n\nclass Main(noodle.Master):\n    """\n    Sample CLI app written with Noodle.\n    """\n\n\nclass Greet(noodle.Command):\n    """\n    Greets someone\n    """\n\n    command_name = "greet"\n    argument = {"name": "Who do you want to greet?"}\n\n    def handler(self):\n        noodle.output(f"Hello {self.argument}")\n\n\napp = Main()\napp.register(Greet)\n\nif __name__ == "__main__":\n    app.run()\n```\n\nCalling the script:\n\n```\n$ python cli.py\nSample CLI app written with Noodle.\n\nUsage:\n  command [options] [arguments]\n\nCommands:\n  greet           Greets someone\n```\n\nCalling a command:\n\n```\n$ python cli.py greet\nHelp:\n  Greets someone\n\nUsage:\n  greet [options] [arguments]\n\nArguments:\n  name            Who do you want to greet?\n```\n\nCalling the command and the argument:\n\n```\n$ python cli.py greet Charles\nHello Charles\n```',
    'author': 'wilfredinni',
    'author_email': 'carlos.w.montecinos@gmail.com',
    'url': 'https://github.com/wilfredinni/noodle',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
