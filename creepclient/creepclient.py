"""CLI client for creep"""

import cmd # Command interpreter logic. Gives us the base class for the client
import inspect # Functions to inspect live objects
import json # JSON encoder and decoder
import os # Miscellaneous operating system interfaces
import shutil # High-level file operations
import subprocess # Spawn subprocesses, connect in/out pipes, obtain return codes
import sys # System specific parameters and functions

from qi.console.client import Client
from entity.package import Package

class CreepClient(Client, cmd.Cmd):
    """Creep Mod Package Manager Client"""

    # Version of this client
    VERSION = '0.0.2'

    # Absolute path where this client is installed
    installdir = ''

    # Absolute path to the dotfile for this client
    appdir = ''

    # Absolute path to the minecraft dir
    minecraftdir = ''

    repository = {}

    def __init__(self, **kwargs):
        """Constructor"""
        cmd.Cmd.__init__(self)
        Client.__init__(self, **kwargs)

        self.updateVersionWithGitDescribe()
        self.updatePaths()

        print "Creep v{}".format(self.VERSION)

        self.readRegistry()

    def do_list(self, args):
        """List available packages (mods)
Usage: creep list
"""

        packages = self.repository
        for package in packages:
            print packages[package]

    def do_install(self, args):
        """Install a package (mod)
Usage: creep install <packagename>

Example: creep install thecricket/chisel2 
"""

        package = self.fetch_package(args)
        if not package:
            return 1

        cachedir = self.appdir + os.sep + 'cache'
        if not os.path.isfile(cachedir + os.sep + package.filename):
            print "Downloading package {0} from {1}".format(package.name, package.get_download_location())
            package.download(cachedir)

        savedir = self.minecraftdir + os.sep + package.installdir 
        shutil.copyfile(cachedir + os.sep + package.filename, savedir + os.sep + package.filename)

        print "Installed mod '{0}' in '{1}'".format(package.name, savedir + os.sep + package.filename)

    def do_uninstall(self, args):
        """Uninstall a package (mod)
Usage: creep uninstall <packagename>

Example: creep uninstall thecricket/chisel2 
"""

        package = self.fetch_package(args)
        if not package:
            return 1

        savedir = self.minecraftdir + os.sep + package.installdir 
        os.remove(savedir + os.sep + package.filename)
        print "Removed mod '{0}' from '{1}'".format(package.name, savedir)

    def fetch_package(self, name):
        if name == '':
            print 'Missing package name'
            return False
        if name not in self.repository:
            print 'Unknown package {}'.format(name)
            return False
        
        return self.repository[name]

    def readRegistry(self):
        registry = json.load(open(self.installdir + os.sep + 'registry.json'))

        repository = {}
        for namekey in registry['packages']:
            for versionkey in registry['packages'][namekey]:
                data = registry['packages'][namekey][versionkey]
                package = Package()
                package.name = data['name']
                package.version = data['version']
                package.description = data['description']
                package.keywords = data['keywords']
                package.require = data['require']
                package.filename = data['filename'] if 'filename' in data else ''
                package.url = data['url'] if 'url' in data else ''
                package.author = data['author']
                package.homepage = data['homepage']
                repository[package.name] = package

        self.repository = repository

    def updatePaths(self):
        self.installdir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

        self.appdir = self.getHomePath('.creep')
        if not os.path.isdir(self.appdir):
            os.mkdir(self.appdir)

        if not os.path.isdir(self.appdir + os.sep + 'cache'):
            os.mkdir(self.appdir + os.sep + 'cache')

        if sys.platform[:3] == 'win':
            self.minecraftdir = self.getHomePath('AppData\\Roaming\\.minecraft')
        else:
            self.minecraftdir = self.getHomePath('.minecraft')

        if not os.path.isdir(self.minecraftdir + os.sep + 'mods'):
            os.mkdir(self.minecraftdir + os.sep + 'mods')

    def getHomePath(self, path=''):
        """Get the home path for this user from the OS"""
        home = os.getenv('HOME')
        if home == None:
            home = os.getenv('USERPROFILE')

        return home + os.sep + path

    def updateVersionWithGitDescribe(self):
        """Update the version of this client to reflect any local changes in git"""

        appdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        try:
            self.VERSION = subprocess.check_output(['git', '-C', appdir, 'describe'], stderr=subprocess.STDOUT).strip()
        except OSError:
            pass
        except subprocess.CalledProcessError:
            # Oh well, we tried, just use the VERSION as it was
            pass
