#!/usr/bin/env python3

# Author: Claymore
# Date: 06-05-2020
#
# This multitool script is used for cleaning the `node_modules` folder,
# cleaning the `build/*` folders and `.cache` and also provides a way
# to automatically reorganize the `build/release` structure
# for production builds
#
# The project root is detected by finding the `config.yaml` file.

# for docopt
"""Claymore's MultiBuild Script (webdev)
This tool allows me (and anyone else) to easily clean, build and configure
various webdev related projects.

Usage:
    multibuild.py [--help]
    multibuild.py clean (Client|Server)
    multibuild.py wipe  (Client|Server)
    multibuild.py postbuild (Client|Server)

Options:
    --help      Shows this help screen

Commands:
    clean (Client|Server)       Cleans the build folder for either the `Client` or the `Server` project
    wipe (Client|Server)        Deleted node_modules, .cache, build folders and lock files
    postbuild (Client|Server)   Restructures the build/release folder.
"""

import errno
import sys
import os
import shutil
import yaml
import time
import subprocess as sp
from dotenv import load_dotenv
from logger import Logger
from pathlib import Path
from docopt import docopt


class Multitool(object):
    def __init__(self, app_name='Client'):
        # name of configuration file
        self.config_filename = 'config.yaml'
        # path to project root
        self.project_root = self.find_project_root()
        # config filepath
        self.config_path = self.project_root / self.config_filename
        # configuration data
        self.config = self.get_config_data()

        # decide which app we're dealing with. this is set in the config.yaml file
        self.app_name = app_name
        self.app_path = self.project_root / self.app_name

        # directories to be cleaned
        self.build_dir = self.app_path / self.get_config_var('build_dir')
        self.cache_dir = self.app_path / '.cache'
        self.module_dir = self.app_path / 'node_modules'

        # postbuild dirs
        self.release_build_dir = self.build_dir / 'release'
        self.asset_dir = self.release_build_dir / self.get_config_var('asset_dir')
        self.static_dir = self.release_build_dir / self.get_config_var('static_dir')

    def find_project_root(self):
        # retrieves the project root.
        path = Path.cwd()
        Logger.pinfo(f'Current working directory is [{path}]')

        # how many attempts we have before giving up?
        max_dir_attempts = 5
        for _ in range(max_dir_attempts):
            temp_root = path / self.config_filename
            project_root = path
            if temp_root.exists():
                Logger.pinfo(
                    f'Project root found at [{project_root.resolve()}]')
                return project_root
            else:
                path = path.resolve().parent

        Logger.perror(
            f'Project root not found! Make sure you set your paths correctly!')
        Logger.exit(errno.ENOENT)

    def get_config_data(self):
        # parses the yaml config
        Logger.pinfo('Loading project configuration', start='\n')

        with open(self.config_path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            if data is not None:
                return data
            else:
                Logger.perror(f'Could not parse [{self.config_filename}]!')
                Logger.exit(errno.EBADF)

    def find_config_var(self, key, src):
        # recursively goes through the yaml config file
        # and check if a given value is a dict, list or a result
        # we're looking for.

        for k, v in (src.items() if isinstance(src, dict)
                     else enumerate(src) if isinstance(src, list)
                     else []):
            if k == key:
                yield v
            elif isinstance(v, (dict, list)):
                for result in self.find_config_var(key, v):
                    yield result

    def get_config_var(self, key):
        # internally calls into `self.find_config_var`
        for result in self.find_config_var(key, self.config):
            if result is not None:
                Logger.pinfo(f'[{key}] is [{result}]')
                return result
            else:
                Logger.perror(f'[{key}] not found in [{self.config_filename}]')
                Logger.exit(errno.ENODATA)

    def clean_dir(self, path):
        Logger.pinfo(f'Deleting [{path.name}]', start='\n')
        if path.exists():
            # for each file and directory in the tree
            # unlink and/or remove it
            for filename in os.listdir(path):
                file_path = path.joinpath(filename)
                try:
                    if file_path.is_file() or file_path.is_symlink():
                        os.unlink(file_path)
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                except Exception as e:
                    Logger.perror(f'Failed to remove [{file_path}]. {e}')
                    Logger.exit(errno.EPERM)

            # remove the build folder itself
            shutil.rmtree(path)
        else:
            Logger.perror(f'[{path}] was not found! Check your paths in [{self.config_filename}]')
            Logger.exit(errno.ENOENT)

    def partial_clean(self):
        self.clean_dir(self.build_dir)
        Logger.pinfo('Clean-up complete!', start='\n')

    def full_clean(self):
        # defaults to npm locks
        lock_file = 'package-lock.json'
        package_manager = self.get_config_var('package_manager')
        if package_manager == 'yarn':
            lock_file = 'yarn.lock'

        lock = self.app_path / lock_file
        if lock.exists():
            try:
                os.unlink(lock)
            except Exception as e:
                Logger.perror(f'Failed to remove [{lock}]. {e}')
                Logger.exit(errno.EPERM)
        else:
            Logger.perror(f'No lockfile found!')
            Logger.exit(errno.ENOENT)

        clean_dirs = [self.build_dir, self.cache_dir, self.module_dir]
        for path in clean_dirs:
            self.clean_dir(path)

        Logger.pinfo('Full clean-up complete!', start='\n')

    def map_files(self):
        Logger.pinfo('Collecting files by their extensions', start='\n')

        if (not self.build_dir.exists()) or (not self.release_build_dir.exists()):
            Logger.perror('Production build not found!')
            Logger.exit(errno.ENOENT)

        # create necessary directories
        if not self.asset_dir.exists():
            self.asset_dir.mkdir()
        if not self.static_dir.exists():
            self.static_dir.mkdir()

        # retrieve static source files
        html_files = list(self.release_build_dir.glob('*.html'))
        css_files = list(self.release_build_dir.glob('*.css'))
        css_map_files = list(self.release_build_dir.glob('*.css.map'))
        js_files = list(self.release_build_dir.glob('*.js'))
        js_map_files = list(self.release_build_dir.glob('*.js.map'))
        resources = list(self.release_build_dir.glob('*.*'))

        # retrieve assets that do not match above static sources
        static_sources = html_files + css_files + css_map_files + js_files + js_map_files
        assets = list(set(resources) - set(static_sources))
        for asset in assets:
            if asset.is_dir():
                assets.remove(asset)

        Logger.pinfo('Mapped files: ')
        for file in sorted(resources):
            Logger.pinfo(f'{file.name}')

        # Map necessary files to the main class
        self.html_files = html_files
        self.css_files = css_files
        self.css_map_files = css_map_files
        self.js_files = js_files
        self.js_map_files = js_map_files
        self.resources = resources
        self.static_sources = static_sources
        self.assets = assets

    def modify_html(self):
        # this monster function does a "fake" in-place modification
        # to paths inside the main `index.html` file
        temp_file = list()
        for index_path in self.html_files:
            with open(index_path) as file:
                for line in file:
                    # replace all backslashes with forward slashes for convenience
                    if '\\' in line:
                        line = line.replace('\\', '/')
                    temp_file.append(line)

        # iterate over the file, look for filenames
        # and replaces them with new paths
        for index in range(0, len(temp_file)):
            for resource in self.resources:
                file = resource.name
                line = temp_file[index]
                if (file in line) and (not 'static' in line):
                    # replace .css and .css.map paths
                    if '.css' in line or '.css.map' in line:
                        temp_file[index] = line.replace(file, str(Path('.') / self.static_dir.name / file))
                    # replace .js and .js.map paths
                    elif ('.js' in line or '.js.map' in line) and (not 'manifest' in line):
                        temp_file[index] = line.replace(file, str(Path('.') / self.static_dir.name / file))
                    # don't replace manifest file paths
                    elif ('__' in line) and ('manifest' in line):
                        temp_file[index] = line
                    # if none of the paths match, it must be an asset
                    else:
                        for asset in self.assets:
                            if (asset.suffix in line) and (not '__' in line) and (not self.asset_dir.name in line):
                                temp_file[index] = line.replace(file, str(Path('.') / self.asset_dir.name / file))

        # open the same file and save the changes
        for index_path in self.html_files:
            with open(index_path, 'w') as file:
                for line in temp_file:
                    # replace all backslashes with forward slashes for convenience
                    if '\\' in line:
                        line = line.replace('\\', '/')
                    file.write(line)

    def move_files(self, file_list, dest):
        # moves a list of files to a specific destination
        for file in file_list:
            try:
                # handle the edge case of manifest files first
                # this is done so that they don't get replaced and stay where they are
                # (since they're already in their own special directory)
                if '__' in str(file):
                    file.replace(file.name)
                else:
                    file.replace(dest / file.name)
            except Exception as e:
                Logger.perror(f'Could not move file [{file}] to [{dest}]. {e}')
                Logger.exit(errno.EPERM)

    def postbuild(self):
        Logger.pinfo('Preparing for post build restructure', start='\n')

        # Map necessary files
        self.map_files()

        # alter the html to reflect new paths
        self.modify_html()

        # move files to new destination
        self.move_files(self.css_files, self.static_dir)
        self.move_files(self.css_map_files, self.static_dir)
        self.move_files(self.js_files, self.static_dir)
        self.move_files(self.js_map_files, self.static_dir)
        self.move_files(self.assets, self.asset_dir)

        Logger.pinfo('Post build complete!', start='\n')


def main():
    args = docopt(__doc__, version="0.0.1")

    for k, v in args.items():
        if v is True and k == 'clean':
            for k, v in args.items():
                if v is True and k == 'Client':
                    tool = Multitool('Client')
                    tool.partial_clean()
                elif v is True and k == 'Server':
                    tool = Multitool('Server')
                    tool.partial_clean()
        elif v is True and k == 'wipe':
            for k, v in args.items():
                if v is True and k == 'Client':
                    tool = Multitool('Client')
                    tool.full_clean()
                elif v is True and k == 'Server':
                    tool = Multitool('Server')
                    tool.full_clean()
        elif v is True and k == 'postbuild':
            for k, v in args.items():
                if v is True and k == 'Client':
                    tool = Multitool('Client')
                    tool.postbuild()
                elif v is True and k == 'Server':
                    tool = Multitool('Server')
                    tool.postbuild()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # if no arguments were provided
        # provide a help command.
        sys.argv.append('--help')

    main()
