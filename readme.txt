This utility is for dynamically generating deployment configuration files for multiple environments.
When you update configuration files, please make sure you run it locally and verify generated configuration files.

Basic folder structure:
- variable_resolver.py
- settings
  - _all
  - dev
  - ...
  - prod
- templates
  - _all
  - dev
  - ...
  - prod
- output


Folder name conventions:
_all: this folder contains files apply to all targets.
env folder: can be anything and you can define as many folders as you want e.g. intdev, local, prod

Templates:
The utility uses Python jinja2 template engine, variable syntax is {{ variable key(supports namespace) }}
Example: {{ JVM.Startup }}, {{ landing_page_port }}

Settings:
Should create folder for each env(e.g. local, intdev or prod) under "settings" folder, "_all" applies to all targets.
Settings supports ini/json/yaml format, accepts ".ini", ".json" and ".yml" only.
You can create as many setting files as you want, but all variable keys should be unique.
Eventually the utility merges all setting files and OS env variables to a single dictionary before apply it to all template files.
Priorities(from highest to lowest) when multiple definitions for same variable name
- Variables defined in specific target folder
- Variables defined in "_all" folder
- OS environment variables

Output:
By default the utility will generate configuration files under "output" sub folder, but you can specify output folder with parameter.
Please note: the utility will not clean output folder before generating files, but will overwrite if there is same file.
This folder is not included in source control.


Running env:
1. Need python 3
2. Install dependencies for python libraries
  pip install jinja2
  pip install ruamel.yaml

3. Run utility
For help:
 python create_config.py -h

Examples:
 python variable_resolver.py --env dev
 python variable_resolver.py --env dev --strict
 python variable_resolver.py --env dev /tmp/build_config


