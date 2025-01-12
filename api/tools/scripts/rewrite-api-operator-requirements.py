#!/usr/bin/env python3

import yaml
import sys


API_ENTRY = 'https://github.com/distronode/distronode/tree/devel/api.git#/api_collection/'


def load_yaml_file(fname):
    with open(fname, 'r') as file:
        data = yaml.safe_load(file)
    return data


def write_yaml_file(fname, data):
    with open(fname, 'w') as file:
        yaml.dump(data, file)


def replace_api(data, path):
    for entry in data['collections']:
        if entry['name'] == API_ENTRY or entry['name'] == 'api.api':
            entry['name'] = f'file://{path}#/api_collection/'
            entry['type'] = 'git'
            entry.pop('version', None)
            return data

    raise ValueError(f"Failed to find {API_ENTRY} in {data}")


def run(fname, api_path):
    write_yaml_file(fname, replace_api(load_yaml_file(fname), api_path))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])
    else:
        print(f"Usage: {sys.argv[0]} <api-operator-molecule-requirements.yml> <api-git-path>", file=sys.stderr)
