# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['whiteless', 'whiteless.templatetags']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['Django>=1.11,<2.0'],
 ':python_version >= "3.5" and python_version < "4.0"': ['Django>=2.0,<3.0']}

setup_kwargs = {
    'name': 'django-whiteless',
    'version': '0.1.3',
    'description': 'Django template tags for dealing with pesky whitespaces',
    'long_description': '# django-whiteless\n\nDjango template tags which deal with pesky whitespaces!\n\n[![CircleCI](https://circleci.com/gh/denizdogan/django-whiteless/tree/master.svg?style=svg)](https://circleci.com/gh/denizdogan/django-whiteless/tree/master)\n\n## Installation\n\nInstall the latest version from PyPI:\n\n```bash\n$ pip install django-whiteless\n```\n\nAdd `"whiteless"` to `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = (\n    # ...\n    "whiteless",\n)\n```\n\n## Usage\n\nThe library consists of two template tags, `{% whiteless %}` and `{% eof %}`.\nThis is how you use them.\n\n### Remove all whitespaces\n\n```djangotemplate\n{% whiteless %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove leading whitespaces\n\n```djangotemplate\n{% whiteless leading %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove trailing whitespaces\n\n```djangotemplate\n{% whiteless trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove leading and trailing whitespaces\n\n```djangotemplate\n{% whiteless leading trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Replace whitespaces with a single space\n\n```djangotemplate\n{% whiteless space %}\n    ...\n{% endwhiteless %}\n```\n\nNote that if there are leading or trailing whitespaces in the block, those will\nalso be replaced by a single space. In order to remove leading and trailing\nwhitespaces and replace all other whitespaces with a single space, use:\n\n```djangotemplate\n{% whiteless space leading trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove trailing whitespaces at end of file\n\n```djangotemplate\nHello there!{% eof %}\n```\n\nThis is useful if e.g. your project style guide requires all files to end with\na newline but that causes issues with your template.\n\nNote that `{% eof %}` cannot be used inside other tags. It only removes\nwhitespaces that immediately follow itself.\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'Deniz Dogan',
    'author_email': 'denizdogan@users.noreply.github.com',
    'url': 'https://github.com/denizdogan/django-whiteless',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
