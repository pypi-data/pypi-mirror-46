# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['manageconf']

package_data = \
{'': ['*']}

install_requires = \
['anyconfig>=0.9.8,<0.10.0', 'boto3>=1.9,<2.0']

setup_kwargs = {
    'name': 'manageconf',
    'version': '1.1.1',
    'description': 'Builds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.',
    'long_description': '# Manage Conf\n\n[![CircleCI](https://circleci.com/gh/sam-atkins/manageconf/tree/main.svg?style=svg)](https://circleci.com/gh/sam-atkins/manageconf/tree/main)\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nBuilds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.\n\nThe config object merges in config, overriding any previous key/value pairs, in the following order:\n\n- ENV\n- default config: default.json\n- stage config: {stage}.json\n- remote config: remote_settings (AWS param store)\n\nAvailable to download as a package on [PyPi](https://pypi.org/project/manageconf/).\n\n### Settings Files\n\nSet an environment variable with the key name `project_config_dir`. It is important this is set before the package is imported. The value of `project_config_dir` should be the location of your `/settings` folder.\n\nSet-up your settings folder, adding in configuration to the appropriate file.\n\n```bash\n.\n├── settings                  <-- Settings folder\n│\xa0\xa0 ├── default.json          <-- default configuration\n│\xa0\xa0 ├── {stage}.json          <-- stage specific configuration e.g. `local`\n│\xa0\xa0 └── {stage}.json          <-- stage specific configuration e.g. `dev`\n```\n\nExample configuration:\n\n#### default.json\n```json\n{\n  "project_name": "example-project",\n  "DEBUG": false\n}\n```\n\n##### local.json\n```json\n{\n  "DEBUG": true,\n  "use_remote_settings": false\n}\n```\n\nLocal config object:\n\n```python\n{\n    "project_name": "example-project",\n    "DEBUG": True,\n    "use_remote_settings": False\n}\n```\n\n##### dev.json\n\n```json\n{\n  "use_remote_settings": true\n}\n```\n\nDev config object:\n\n```python\n{\n    "project_name": "example-project",\n    "DEBUG": True,\n    "use_remote_settings": True\n    # and any remote settings from AWS param store\n}\n```\n\n\n### AWS Param Store\n\n#### Project config\n\nAdd parameters in your AWS account with paths that match this pattern:\n\n`/{project_name}/{stage}/`\n\nIf you set `"use_remote_settings": true` in a remote `{stage}.json` config file, the package will attempt to fetch the parameters from the store that have the specified base path. Using the example configuration above, the path would be:\n\n```\n/example-project/dev/\n```\n\n#### Global service directory config\n\nAdd parameters in your AWS account with paths that match this pattern:\n\n`/global/{stage}/service_directory/`\n\nSet `"global_service_directory": true` in a remote `{stage}.json` config file.\n\nGlobal service directory config for the `{stage}` will be merged in.\n\n### Usage\n\nMake sure `project_config_dir` is set before importing the library.\n\n```python\nfrom manageconf import Config, get_config\n\nSECRET_KEY = get_config("SECRET_KEY")\nDEBUG = get_config("DEBUG", True)\n# default values are an optional second arg and will\n# be used if the param cannot be found in the config object\n```\n\n## Development\n\n### Install\n\nRequires [Poetry](https://poetry.eustace.io).\n\n```bash\n# create a Python3 virtual environment\nvirtualenv -p python3 env\n\n# activate the virtual env\nsource env/bin/activate\n\n# install requirements\npoetry install\n```\n\n### Tests\n\n```bash\n# run tests\npytest -vv\n\n# coverage report in the Terminal\npytest --cov=manageconf tests/\n\n# coverage report in HTML\npytest --cov-report html --cov=manageconf tests/\n```\n',
    'author': 'Sam Atkins',
    'author_email': 'samatkins@outlook.com',
    'url': 'https://github.com/sam-atkins/manageconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
