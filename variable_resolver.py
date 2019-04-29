import os, sys
import configparser
import argparse
from ruamel.yaml import YAML
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Undefined, StrictUndefined
from shutil import copyfile

# application settings
APP_INCLUDE_ENV_VARIABLE = True

# directories definition
ALL_DIR = '_all'
TEMPLATE_DIR = 'templates'
SETTING_DIR = 'settings'
DEFAULT_OUTPUT_DIR = 'output'

# full path
APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(APP_PATH, TEMPLATE_DIR)
SETTING_PATH = os.path.join(APP_PATH, SETTING_DIR)
DEFAULT_OUTPUT_PATH = os.path.join(APP_PATH, DEFAULT_OUTPUT_DIR)


# get all files in a directory with full path
def get_files_full_path(path):
    files_path = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            files_path.append(os.path.join(path, file))
    return files_path

# get all files in specified folder
def get_shared_files(path):
    all_env_path = os.path.join(path, ALL_DIR)
    return get_files_full_path(all_env_path)


# get all files in specified folder
def get_env_files(path, env):
    env_path = os.path.join(path, env)
    return get_files_full_path(env_path)


# read environment variables
def read_env_variables():
    return os.environ


# read setting from ini style file, section is must
def read_ini_config(file):
    ini = configparser.ConfigParser()
    ini.read(file)
    return ini


# read setting from yaml or json file
def read_yaml_or_json_config(file):
    yaml = YAML(typ='safe')
    return yaml.load(Path(file))


# get setting from file
def get_settings(setting_path):
    settings = {}
    if setting_path.endswith('.ini'):
        settings = read_ini_config(setting_path)
    elif setting_path.endswith('.json') or setting_path.endswith('.yml'):
        settings = read_yaml_or_json_config(setting_path)
    return settings


# update templates and output
def update_and_output_templates(template_path, template_files, settings, output_dir, strict_mode):
    if strict_mode:
        template_env = Environment(autoescape=False, loader=FileSystemLoader(template_path), undefined=StrictUndefined)
    else:
        template_env = Environment(autoescape=False, loader=FileSystemLoader(template_path))
    for template_file in template_files:
        template_file_name = os.path.basename(template_file)
        updated_template = template_env.get_template(template_file_name).render(settings)
        output_file = os.path.join(output_dir, template_file_name)
        with open(output_file, 'w') as f:
            f.write(updated_template)
            print('- generated %s' % template_file_name)


# start
parser = argparse.ArgumentParser()
parser.add_argument('--env', help='[Mandatory] target env')
parser.add_argument('--out', help='[Optional] output path')
parser.add_argument('--strict', default=False, action='store_true', help='[Optional] Cause error for missing variables in strict mode, default value is False')
args = parser.parse_args()

if args.env is None:
    print('Please use -h option for help!')
    exit(1)

# config setting path
env_name = args.env

# output path
output_path = DEFAULT_OUTPUT_PATH
if args.out is not None:
    output_path = args.out
if not os.path.exists(output_path):
    os.makedirs(output_path)

print('Generating configuration files at %s' % output_path)

# 1. get all settings
all_settings = {}
if APP_INCLUDE_ENV_VARIABLE:
    all_settings.update(read_env_variables())
shared_setting_files = get_shared_files(SETTING_PATH)
env_setting_files = get_env_files(SETTING_PATH, env_name)
for setting_file in shared_setting_files:
    all_settings.update(get_settings(setting_file))
for setting_file in env_setting_files:
    all_settings.update(get_settings(setting_file))

# 2. update all templates based on settings, then output to files
shared_templates = get_shared_files(TEMPLATE_PATH)
env_templates = get_env_files(TEMPLATE_PATH, env_name)
update_and_output_templates(os.path.join(TEMPLATE_PATH, ALL_DIR), shared_templates, all_settings, output_path, args.strict)
update_and_output_templates(os.path.join(TEMPLATE_PATH, env_name), env_templates, all_settings, output_path, args.strict)
