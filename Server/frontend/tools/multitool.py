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
from pathlib import Path
from collections import Counter
from colorama import Fore, Back, Style


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
        print(
            f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} We're currently in: {Fore.GREEN}{Path.cwd()}{Style.RESET_ALL}")
        print(
            f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Trying to find the project root...{Style.RESET_ALL}\n")

        # The project root is determined by the package.json file
        # so look for it, and once it's found, return it
        path = Path.cwd()
        for _ in range(self.max_dir_attempts):
            temp_root = Path.joinpath(path, 'package.json')
            project_root = path
            if temp_root.exists():
                print(
                    f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Project root found at: {Fore.GREEN}[{project_root}]{Style.RESET_ALL}\n")
                return project_root
            else:
                path = path.parent

    def clean_dir(self, where):
        print(
            f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Deleting {Style.BRIGHT}{Fore.RED}[{where}]{Style.RESET_ALL}\n")
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
                    print(
                        f"{Style.BRIGHT}{Fore.RED}[ERROR]:{Style.RESET_ALL} Failed to delete {Style.BRIGHT}[{file_path}]\n{Style.BRIGHT}{Fore.RED}[{e}]{Style.RESET_ALL}")

            # Remove the build folder itself
            shutil.rmtree(where)
            print(
                f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Clean-up complete!{Style.RESET_ALL}")
        else:
            # If this happens, make sure to check your paths!
            print(
                f"{Style.BRIGHT}{Fore.RED}[ERROR]:{Style.RESET_ALL} Path not found! \n{Style.BRIGHT}[{where}]{Style.RESET_ALL}")

    def clean(self):
        self.clean_dir(self.build_dir)

    def wipeout(self):
        print(
            f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Preparing for total wipe...{Style.RESET_ALL}")

        # Remove the lock files too.
        # NOTE: only supports yarn and npm
        lockFiles = ["yarn.lock", "package-lock.json"]
        for lock in lockFiles:
            file = Path(self.project_root / lock)
            os.remove(file)

        for path in self.wipe_paths:
            self.clean_dir(path)

    # This monster function saves an html file to a temporary array,
    # modifies the temporary array paths,
    # puts it back into the file and calls it a day
    #
    # NOTE: I tried to do this using an `in_place` library
    # which let's you to do file i/o on the same file in one-go
    # but it ended up being a total failure.
    # If anyone knows any better solution, let me know
    def alterHTML(self):

        # Save the contents of the file, line per line,
        # into a temporary array
        temp_file = []
        for index in self.html_files:
            with open(str(index)) as file:
                modline = ''
                for line in file:
                    # Replace all backslashes with forward slashes for convenience sake
                    if '\\' in line:
                        modline = line.replace('\\', '/')
                    else:
                        modline = line
                    temp_file.append(modline)

        # Iterate over the file, all the filenames
        # all the assets extensions and replace filenames in index.html
        # with new paths and move them up
        for index in range(0, len(temp_file)):
            for resource in self.all_files:
                filename = resource.name
                line = temp_file[index]
                if filename in line and not 'static' in line:
                    # Replace .css and .css.map filepaths with static paths + filename
                    if '.css' in line or '.css.map' in line:
                        temp_file[index] = line.replace(
                            filename, str(Path('.') / self.static_path.name / filename))
                    # Replace .js and .js.map filepaths with static paths + filename
                    elif ('.js' in line or '.js.map' in line) and not('manifest' in line):
                        temp_file[index] = line.replace(
                            filename, str(Path('.') / self.static_path.name / filename))
                    # DON'T replace .manifest filepaths.
                    elif '__' in line and 'manifest' in line:
                        temp_file[index] = line
                    else:
                        for exts in self.assets:
                            # Add relative directories to assets too.
                            if (exts.suffix in line and not '__' in line) and not ('assets' in line):
                                temp_file[index] = line.replace(
                                    filename, str(Path('.') / self.assets_path.name / filename))

        # Open the same file and save it line by line
        for index in self.html_files:
            with open(str(index), 'w') as file:
                modline = ''
                for line in temp_file:
                    # Replace all backslashes with forward slashes for convenience sake
                    if '\\' in line:
                        modline = line.replace('\\', '/')
                    else:
                        modline = line
                    file.write(modline)

    def moveFiles(self, file_list, dest):
        for file in file_list:
            try:
                if '__' in str(file):
                    file.replace(file.name)
                else:
                    file.replace(dest / file.name)
            except Exception as e:
                print(
                    f"{Style.BRIGHT}{Fore.RED}[ERROR]:{Style.RESET_ALL} Couldn't move file {Style.BRIGHT}[{file}]{Style.RESET_ALL} to  {Style.BRIGHT}[{dest}]{Style.RESET_ALL}\n{Style.BRIGHT}{Fore.RED}[{e}]{Style.RESET_ALL}")

    def postbuild(self):
        print(
            f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Preparing for restructure of build folders...{Style.RESET_ALL}")
        # Make sure the build folder and the release path exist...
        if not(self.build_dir.exists()) or not(self.release_path.exists()):
            print(
                f"{Style.BRIGHT}{Fore.RED}[ERROR]:{Style.RESET_ALL} Production build not found!{Style.RESET_ALL}")
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
            self.relevant_files = self.html_files + self.css_files + \
                self.js_files + self.css_map_files + self.js_map_files
            self.all_files = sorted(self.release_path.glob('*'))

            # Get all the other assets
            self.assets = list(set(self.all_files) - set(self.relevant_files))
            for asset in self.assets:
                if asset.is_dir():
                    self.assets.remove(asset)

            print(
                f"\n{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Postbuild statistics: {Style.RESET_ALL}")
            print(
                f"{Style.BRIGHT}{Fore.BLUE}[POSTBUILD]:{Style.RESET_ALL} [*.html] files: {Style.RESET_ALL}")
            for file in self.html_files:
                print(f"{Style.DIM}{file.name}{Style.RESET_ALL}")
            print()

            print(
                f"{Style.BRIGHT}{Fore.BLUE}[POSTBUILD]:{Style.RESET_ALL} [*.css] and [*.css.map] files: {Style.RESET_ALL}")
            for file in (self.css_files + self.css_map_files):
                print(f"{Style.DIM}{file.name}{Style.RESET_ALL}")
            print()

            print(
                f"{Style.BRIGHT}{Fore.BLUE}[POSTBUILD]:{Style.RESET_ALL} [*.js] and [*.js.map] files: {Style.RESET_ALL}")
            for file in (self.js_files + self.js_map_files):
                print(f"{Style.DIM}{file.name}{Style.RESET_ALL}")
            print()

            print(
                f"{Style.BRIGHT}{Fore.BLUE}[POSTBUILD]:{Style.RESET_ALL} Assets: {Style.RESET_ALL}")
            for file in self.assets:
                print(f"{Style.DIM}{file.name}{Style.RESET_ALL}")
            print()

            # Modify html code to accomodate for new paths
            self.alterHTML()

            # Move all the files
            self.moveFiles(self.css_files, self.static_path)
            self.moveFiles(self.css_map_files, self.static_path)
            self.moveFiles(self.js_files, self.static_path)
            self.moveFiles(self.js_map_files, self.static_path)
            self.moveFiles(self.assets, self.assets_path)

            print(
                f"{Style.BRIGHT}{Fore.GREEN}[INFO]:{Style.RESET_ALL} Post build complete!{Style.RESET_ALL}")


def usage():
    print("Claymore's MultiTool")
    print("options: ")
    print("\thelp: \t\tshows this help menu")
    print("\tclean: \t\tperforms a basic clean-up of build directories")
    print("\twipe: \t\tperforms a complete clean-up")
    print("\tpostbuild: \treorganizes project structure of the release build")


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
            usage()
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
