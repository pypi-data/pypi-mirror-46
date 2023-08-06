# Manage Conf

[![CircleCI](https://circleci.com/gh/sam-atkins/manageconf/tree/main.svg?style=svg)](https://circleci.com/gh/sam-atkins/manageconf/tree/main)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Description

Builds a config object based on environment variables, settings files and (optional) parameters stored in AWS System Manager Parameter Store.

The config object merges in config, overriding any previous key/value pairs, in the following order:

- ENV
- default config: default.json
- stage config: {stage}.json
- remote config: remote_settings (AWS param store)

Available to download as a package on [PyPi](https://pypi.org/project/manageconf/).

### Settings Files

Set an environment variable with the key name `project_config_dir`. It is important this is set before the package is imported. The value of `project_config_dir` should be the location of your `/settings` folder.

Set-up your settings folder, adding in configuration to the appropriate file.

```bash
.
├── settings                  <-- Settings folder
│   ├── default.json          <-- default configuration
│   ├── {stage}.json          <-- stage specific configuration e.g. `local`
│   └── {stage}.json          <-- stage specific configuration e.g. `dev`
```

Example configuration:

#### default.json
```json
{
  "project_name": "example-project",
  "DEBUG": false
}
```

##### local.json
```json
{
  "DEBUG": true,
  "use_remote_settings": false
}
```

Local config object:

```python
{
    "project_name": "example-project",
    "DEBUG": True,
    "use_remote_settings": False
}
```

##### dev.json

```json
{
  "use_remote_settings": true
}
```

Dev config object:

```python
{
    "project_name": "example-project",
    "DEBUG": True,
    "use_remote_settings": True
    # and any remote settings from AWS param store
}
```


### AWS Param Store

#### Project config

Add parameters in your AWS account with paths that match this pattern:

`/{project_name}/{stage}/`

If you set `"use_remote_settings": true` in a remote `{stage}.json` config file, the package will attempt to fetch the parameters from the store that have the specified base path. Using the example configuration above, the path would be:

```
/example-project/dev/
```

#### Global service directory config

Add parameters in your AWS account with paths that match this pattern:

`/global/{stage}/service_directory/`

Set `"global_service_directory": true` in a remote `{stage}.json` config file.

Global service directory config for the `{stage}` will be merged in.

### Usage

Make sure `project_config_dir` is set before importing the library.

```python
from manageconf import Config, get_config

SECRET_KEY = get_config("SECRET_KEY")
DEBUG = get_config("DEBUG", True)
# default values are an optional second arg and will
# be used if the param cannot be found in the config object
```

## Development

### Install

Requires [Poetry](https://poetry.eustace.io).

```bash
# create a Python3 virtual environment
virtualenv -p python3 env

# activate the virtual env
source env/bin/activate

# install requirements
poetry install
```

### Tests

```bash
# run tests
pytest -vv

# coverage report in the Terminal
pytest --cov=manageconf tests/

# coverage report in HTML
pytest --cov-report html --cov=manageconf tests/
```
