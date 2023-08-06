# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ghost2md']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ghost2md = ghost2md.ghost2md:main']}

setup_kwargs = {
    'name': 'ghost2md',
    'version': '0.1.0',
    'description': 'Convert Ghost articles to markdown files',
    'long_description': "\n# Ghost2md\n\nA simple utility for converting the articles stored in a ghost backup file to Markdown. `ghost2md` will convert posts and pages to markdown files and will include any tags associated with the post as well.\n\n## Motivation\n\nI needed a simple tool for converting all my Ghost articles to markdown files which would be used by `Gatsby.js`. Didn't find any tools that produced markdown to my liking. Thus, `ghost2md` was born.\n\n## Requirements\n\n* Python 3.4+\n\n## Installation\n\n### Via pip\n`pip3 install ghost2md --user`\n\n### Via Poetry\n`poetry install` (Run command inside of `ghost2md`)\n\n## Contributing\nAny feedback or ideas are welcome! Want to improve something? Create a pull request!\n\n1. Fork it!\n2. Create your feature branch: `git checkout -b my-new-feature`\n3. Commit your changes: `git commit -am 'Add some feature'`\n4. Push to the branch: `git push origin my-new-feature`\n5. Submit a pull request :D\n",
    'author': 'Michael Dubell',
    'author_email': 'michael@dubell.io',
    'url': 'https://github.com/mjdubell/ghost2md',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
