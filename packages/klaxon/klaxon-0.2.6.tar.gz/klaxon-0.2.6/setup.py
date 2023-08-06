# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['klaxon']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

extras_require = \
{'notifiers': ['notifiers>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['klaxon = klaxon:main']}

setup_kwargs = {
    'name': 'klaxon',
    'version': '0.2.6',
    'description': 'Use osascript to send notifications.',
    'long_description': '# klaxon\n\nSend Mac OS (or [notifiers][notifiers]) notifications from the terminal or Python programs.\n\nThis is especially useful for when you want a push notification \nfor some long-running background task.\n\nSimilar to the [terminal-notifier ruby gem][terminal-notifier],\nbut posix-compliant and able to send notifications via\nthe [notifiers][notifiers] library.\n\n![hello-klaxon](static/recording.gif)\n\n## Installation\nFor command-line use, the recommended method of installation is through [pipx].\n```bash\npipx install klaxon\n```\nNaturally, klaxon can also be pip-installed.\n```bash\npip install klaxon\n```\n\n## Usage\n\n### terminal\n\n```bash\n# blank notification\nklaxon\n# with custom message\nklaxon --message "this is the message body"\n# pipe message from other program\necho "this is the message body" | klaxon --\n```\n\n### python\n\n```python\nfrom klaxon import klaxon, klaxonify\n\n# send a notification\n\nklaxon(\n    title=\'hello, klaxon\',\n    subtitle=\'hola\',\n    message=\'it me\'\n)\n\n# we can decorate our functions to have\n# them send notifications at termination\n\n@klaxonify\ndef hello(name=\'world\'):\n    return f\'hello, {name}\'\n\n\n@klaxonify(title=\'oh hai\', output_as_message=True)\ndef foo():\n    return "This will be the message body."\n\n```\n\n## Non-MacOS Notifications \n\n### i.e. mobile | email | slack\n\nYou\'ll need to install klaxon with the `notifiers` extra.\n\n```bash\npipx install klaxon[notifiers]\n```\n\nYou will need a `~/.config/klaxon/config.toml` or `pyproject.toml` file with the\n`tool.klaxon` namespace configured at the top level. Values from the latter will\noverride values in the former.\n\n`enable-notifiers` will need to be set to `true` and you will need a `[[notifiers]]` key.\n\nThe latter will determine the parameters passed to the `notifiers.notify` method.\n\nFor example:\n\n`~/.config/klaxon/config.toml`\n```toml\nenable-notifiers = true\n\n[[notifiers]]\nname = \'slack\'\n# see https://api.slack.com/incoming-webhooks#getting-started\nwebhook_url = {{your webhook url}}\n\n[[notifiers]]\nname = \'pushover\'\nuser = {{your user token}}\ntoken = {{your application token}}\n```\n\nVoila! Now messages sent from klaxon will be pushed to slack and pushover.\n\n\n[terminal-notifier]: https://github.com/julienXX/terminal-notifier\n[pipx]: https://github.com/pipxproject/pipx\n[osascript]: https://apple.stackexchange.com/questions/57412/how-can-i-trigger-a-notification-center-notification-from-an-applescript-or-shel/115373#115373\n[notifiers]: https://github.com/notifiers/notifiers',
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'url': 'https://pypi.org/project/klaxon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
