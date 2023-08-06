#########################################################################################
# FlowTees, tool to automate the conversion of trivial Flow to TS work                  #
# Supports:                                                                             #
#  - Renames files to tsx/ts                                                            #
#  - Ignores node_modules                                                               #
#  - Removing flow decorators (@flow, $StringLitteral, $FlowFixMe)                      #
#  - Remove type keyword from exports and imports                                       #
#  - Renames type keyword to interface keyword when applicable and can handle extends   #
#  - Configures package.json and creates tsconfig.json files                            #
#########################################################################################

import os
import re
from typing import List

import click
from helpers.utilities import (build_file_list, make_tsconfig_base_file,
                               make_tsconfig_build_file, update_package_json)

tsx_keywords = ['\'react\'', 'jsx', 'emotion']
flow_keywords = ['// $StringLitteral',
                 '//$StringLitteral', '//$FlowFixMe', '// $FlowFixMe']


def refactor(contents: List[str]) -> str:
    in_multiline_import = False
    for idx, line in enumerate(contents):
        # Check for flow decorators
        if '// @flow' in line:
            line = ''  # remove line completely
            if contents[idx+1] and not contents[idx+1].split():
                contents[idx+1] = ''
        if any(keyword in line for keyword in flow_keywords):
            line = ''

        # Check import, remove any type keywords
        if in_multiline_import:
            if 'from' in line:
                in_multiline_import = False
            if re.search(r'\btype\b', line):
                line = line.replace('type ', '')
        elif 'import' in line:
            if ';' in line:
                if 'type' in line:
                    line = line.replace('type ', '')
            else:
                in_multiline_import = True
                continue

        # Check type, then convert to interface
        if re.search(r'\btype\b', line):
            if '=' in line:
                # Peek to determine if actually a type
                if not '{' in line or '|' in line:
                    continue

                if '&' in line:
                    line = line.replace('=', 'extends').replace(
                        '& ', '').replace('type', 'interface')
                else:
                    line = line.replace('= ', '').replace('type', 'interface')
            elif 'export' in line:  # if it is declared as an export in an index file
                line = line.replace('type ', '')
            else:
                line = line.replace('type', 'interface')

        contents[idx] = line
    return ''.join(contents)


def process(file_path: str, dry_run: bool = False) -> bool:
    try:
        file_path = os.path.abspath(file_path)
        f = open(file_path, 'r')
        contents = f.readlines()

        if not contents:
            click.secho('%s is empty' % file_path, fg='red')
            return False

        refactored_contents = refactor(contents)

        if not dry_run:
            f = open(file_path, 'w')
            f.write(refactored_contents)

            if any(keyword in refactored_contents for keyword in tsx_keywords):
                new_file_name = file_path.split('.')[0] + '.tsx'
            else:
                new_file_name = file_path.split('.')[0] + '.ts'

            os.rename(file_path, new_file_name)
        return True
    except:
        if not dry_run:
            click.secho('Something went wrong while processing:\n%s' %
                        file_path, fg='red')
        return False


def make_tsconfig_files(root_dir: str):
    if make_tsconfig_base_file(root_dir):
        click.echo('Base tsconfig.json created')
    else:
        click.secho('Could not create base tsconfig.json', fg='red')

    if make_tsconfig_build_file(root_dir):
        click.echo('Build tsconfig.json created')
    else:
        click.secho('Could not create build tsconfig.json', fg='red')


def configure_build(dir):
    # Prompt to create build files
    if click.confirm('Do you want to configure build files?'):
        if update_package_json(dir):
            click.echo('package.json updated to read index.ts')
        else:
            click.secho('package.json could not be updated', fg='red')
        make_tsconfig_files(dir)
        click.secho('\nBuild configuration done!', fg='black', bg='green')
        click.echo()


@click.command()
@click.argument('component_dir')
def main(component_dir: str):
    if not component_dir:
        click.echo('No component directory was provided')

    processed_count = 0

    files = build_file_list(component_dir)

    if len(files) < 1:
        click.echo('Nothing to process')
        configure_build(component_dir)
        return

    # Run a dry run
    list_of_compatible_files = []
    list_of_incompatible_files = []
    for path in files:
        if not process(path, dry_run=True):
            list_of_incompatible_files.append(os.path.relpath(path))
            continue
        list_of_compatible_files.append(os.path.relpath(path))

    # For incompatible files
    num_of_incompatible = len(list_of_incompatible_files)
    if len(list_of_incompatible_files) > 1:
        click.secho('\nThe following files cannot be processed:\n', fg='red')
        click.secho('\n'.join(list_of_incompatible_files), fg='red')
        click.secho('%d files total' %
                    num_of_incompatible, fg='red', bold=True)

    # For compatible files
    num_of_compatible = len(list_of_compatible_files)
    if num_of_compatible > 1:
        click.secho('\nThe list of files will be processed:\n')
        click.secho('\n'.join(list_of_compatible_files), fg='green')
        click.secho('\n%d files total\n' %
                    num_of_compatible, bold=True)

    # Prompt for confirmation
    if click.confirm('Do you want to continue?'):
        for path in list_of_compatible_files:
            if process(path, dry_run=False):
                click.echo('Processed: %s' % os.path.relpath(path))
                processed_count += 1

        click.secho('\nProcessed %d file(s)' %
                    processed_count, fg='black', bg='green')
        click.echo()

    configure_build(component_dir)


if __name__ == "__main__":
    main()
