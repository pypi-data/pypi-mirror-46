# FlowTees utilities to further help with refactoring Flow to TS
import json
import os
from collections import OrderedDict
from typing import List

import click
from helpers.build_files import (get_template_base_tsconfig,
                                 get_template_build_tsconfig)

exclude_directories = ('node_modules')


def load_ordered_json(data):
    if not type(data).__name__ == 'str':
        return json.load(data, object_pairs_hook=OrderedDict)
    return json.loads(data, object_pairs_hook=OrderedDict)


def write_json(file_dir, json_file) -> bool:
    try:
        with open(file_dir, 'w') as writer:
            data = load_ordered_json(json_file)
            json.dump(data, writer, indent=2)
            return True
    except:
        return False


def make_tsconfig_build_file(root_dir) -> bool:
    build_dir = root_dir + '/build/es2015'
    try:
        os.makedirs(build_dir)
    except FileExistsError:
        click.echo(
            'Build directory already exists. No new directories were created.')
    finally:
        build_file = build_dir + '/tsconfig.json'
        try:
            exists = os.path.exists(build_file)
            if exists:
                click.secho(
                    'tsconfig.json in build directory already exists', fg='red')
                if click.confirm('Do you want to override this?'):
                    write_json(build_file, get_template_build_tsconfig())
                    return True
            else:
                write_json(build_file, get_template_build_tsconfig())
                return True
            return False
        except:
            return False


def make_tsconfig_base_file(root_dir) -> bool:
    base_file = root_dir + '/tsconfig.json'
    try:
        exists = os.path.exists(base_file)
        if exists:
            click.secho(
                'tsconfig.json in component root directory already exists', fg='red')
            if click.confirm('Do you want to override this?'):
                write_json(base_file, get_template_base_tsconfig())
                return True
        else:
            write_json(base_file, get_template_base_tsconfig())
            return True
        return False
    except:
        return False


def update_package_json(root_dir) -> bool:
    try:
        package_json = open('%s/package.json' % root_dir, 'r')
        data = load_ordered_json(package_json)
        data["atlaskit:src"] = "src/index.ts"

        package_json = open('%s/package.json' % root_dir, 'w')
        json.dump(data, package_json, indent=2)
        return True
    except:
        click.secho('Something went wrong when updating package.json', fg='red')
        return False


def build_file_list(dir) -> List[str]:
    files = []
    for dir_name, subdir_list, file_list in os.walk(dir, topdown=False):
        # Exclude directories
        if exclude_directories in dir_name:
            continue

        file_list[:] = exclude(file_list, extensions=('.js'))

        # only traverse if there are files
        if len(file_list) > 0:
            for file in file_list:
                file_path = os.path.join(dir_name, file)
                files.append(file_path)
    return files


def exclude(list, hidden=True, extensions='') -> List[str]:
    exclude_prefixes = ('__', '.')
    if not hidden:
        return [item
                for item in list
                if item.endswith(extensions)]
    return [item
            for item in list
            if (not item.startswith(exclude_prefixes)) and item.endswith(extensions)]
