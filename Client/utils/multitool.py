#!/usr/bin/env python3

# Author: Claymore
# Date: 06-05-2020
#
# This multitool script is used for cleaning the `node_modules` folder,
# cleaning the `build/*` folders and `.cache` and also provides a way
# to automatically reorganize the `build/release` structure
# for production builds
#
# The project root is detected via the first directory up the tree that contains the `package.json` file

import sys
import os
import getopt
import shutil
import pprint
import in_place
# import itertools
from pathlib import Path
from collections import Counter


class MultiTool(object):
    def __init__(self):
        # how many directories up to go at max to reach projects root
        self.max_dir_attempts = 5
        # the current path to the project root
        self.project_root = self.set_project_root()
        # path to the `build/*` or `dist/*` folders, change accordingly
        self.build_dir = self.project_root / 'build/'
        # path to `.cache` file and other volatiles if you have them
        self.cache_dir = self.project_root / '.cache/'
        # path to `node_modules`
        self.module_dir = self.project_root / 'node_modules/'
        # All paths for wipeout
        self.wipe_paths = [self.build_dir, self.cache_dir, self.module_dir]

        # Post build stuff
        self.release_path = self.build_dir / 'release'
        # Set your preferences for post build folder structure here
        # Where to put assets?
        self.assets_path = self.release_path / 'assets'
        # Where to put static files?
        self.static_path = self.release_path / 'static'

    def set_project_root(self):
        print(f"We're currently in: {Path.cwd()}\n")
        print(f"Trying to find the project root...")

        # The project root is determined by the package.json file
        # so look for it, and once it's found, return it
        path = Path.cwd()
        for folder in range(self.max_dir_attempts):
            temp_root = Path.joinpath(path, 'package.json')
            project_root = path
            if temp_root.exists():
                print(f"Project root found at: {project_root}\n")
                return project_root
            else:
                path = path.parent

    def clean_dir(self, where):
        print(f"Deleting {where}...\n")
        if where.exists():
            # For each file/link and directory in the folder
            # unlink it and remove the entire tree
            for filename in os.listdir(where):
                file_path = where.joinpath(filename)
                try:
                    if file_path.is_file() or file_path.is_symlink():
                        os.unlink(file_path)
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                # Perhaps no access privileges?
                except Exception as e:
                    print(f'[ERROR]: Failed to delete {file_path}. {e}')

            # Remove the build folder itself
            shutil.rmtree(where)
            print("Clean-up complete!")
        else:
            # If this happens, make sure to check your paths!
            print('[ERROR]: Folder not found! Path: {where}')

    def clean(self):
        self.clean_dir(self.build_dir)

    def wipeout(self):
        print(f"Preparing for total wipe...\n")
        for path in self.wipe_paths:
            self.clean_dir(path)

    # This monster function saves an html file to a temporary array,
    # modifies the temporary array paths,
    # puts it back into the file and calls it a day
    def alterHTML(self):

        # Save the contents of the file, line per line,
        # into a temporary array
        temp_file = []
        for index in self.html_files:
            with open(str(index)) as file:
                for line in file:
                    temp_file.append(line)

        # Iterate over the file, all the filenames
        # all the assets extensions and replace filenames in index.html
        # with new paths and move them up
        for index in range(0, len(temp_file)):
            for resource in self.all_files:
                filename = resource.name
                line = temp_file[index]
                if filename in line and not 'static' in line:
                    if '.css' in line or '.css.map' in line:
                        temp_file[index] = line.replace(filename, str(self.static_path.name / filename))
                    elif ('.js' in line or '.js.map' in line) and (not 'manifest' in line):
                        temp_file[index] = line.replace(filename, str(self.static_path.name / filename))
                    elif '__' in line:
                        pass
                    else:
                        for exts in self.assets:
                            if exts.suffix in line and not '__' in line:
                                temp_file[index] = line.replace(filename, str(self.assets_path.name / filename))

        for index in self.html_files:
            with open(str(index), 'w') as file:
                for line in temp_file:
                    file.write(line)

    def moveFiles(self, file_list, dest):
        for file in file_list:
            try:
                if '__' in str(file):
                    pass
                else:
                    file.replace(dest / file.name)
                    print(dest / file.name)
            except Exception as e:
                print(f"[ERROR]: Couldn't move file {file} to {dest}, {e}")

    def postbuild(self):
        print(f"Preparing for restructure of build folders...\n")
        # Make sure the build folder and the release path exist...
        if not(self.build_dir.exists()) or not(self.release_path.exists()):
            print(f"No production build detected!")
        else:
            # Create necessary directories
            if not (self.assets_path.exists()):
                self.assets_path.mkdir()
            if not (self.static_path.exists()):
                self.static_path.mkdir()

            # Map `.html` files
            self.html_files = list(self.release_path.glob('*.html'))

            # Map `.css` files
            self.css_files = list(self.release_path.glob('*.css'))

            # Map `.js` files
            self.js_files = list(self.release_path.glob('*.js'))

            # Various `.map.*` files
            self.css_map_files = list(self.release_path.glob('*.css.map'))
            self.js_map_files = list(self.release_path.glob('*.js.map'))

            # Combine to later get all the assets
            self.relevant_files = self.html_files + self.css_files + self.js_files + self.css_map_files + self.js_map_files
            self.all_files = sorted(self.release_path.glob('*'))

            # Get all the other assets
            self.assets = list(set(self.all_files) - set(self.relevant_files))
            for asset in self.assets:
                if asset.is_dir():
                    self.assets.remove(asset)

            # Modify html code to accomodate for new paths
            self.alterHTML()

            # Move all the files
            self.moveFiles(self.css_files, self.static_path)
            self.moveFiles(self.css_map_files, self.static_path)
            self.moveFiles(self.js_files, self.static_path)
            self.moveFiles(self.js_map_files, self.static_path)
            self.moveFiles(self.assets, self.assets_path)


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], '', ["help", "clean", "wipe", "postbuild"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    multitool = MultiTool()
    for option in args:
        if option == 'help':
            print('Help should be printed here')
        elif option == 'clean':
            multitool.clean()
        elif option == 'wipe':
            multitool.wipeout()
        elif option == 'postbuild':
            multitool.postbuild()
        else:
            assert False, 'Unhandled option'


if __name__ == "__main__":
    main()
