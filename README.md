# Creep

A Minecraft package manager for mods

    █████████████████
    █░░░░░░░░░░░░░░░█
    █░░████░░░████░░█
    █░░████░░░████░░█
    █░░░░░░███░░░░░░█
    █░░░░███████░░░░█
    █░░░░███████░░░░█
    █░░░░██░░░██░░░░█
    █░░░░░░░░░░░░░░░█
    █████████████████

## Prerequisites

### Minecraft
Of course you need to download and install Minecraft and have valid Minecraft account

### Install Forge 
 - Download Minecraft Forge Installer from http://files.minecraftforge.net/maven/net/minecraftforge/forge/index_1.7.10.html
 - Run the Forge installer
 - Inside Minecraft, create or edit a profile where "Use Version:" is set to
   the forge version just installed

### Install Python
 - For Windows: https://www.python.org/downloads/release/python-279/
   - Download and run installer from above link
   - Make sure to select option "Add python.exe to Path"
   - Verify installation by opening a new command terminal and typing `python --version`

## Installation of Creep

This section will provide some guidance on how to install *creep*

### Installation for Linux/Mac
 - Clone this repo or download a release on the releases page
 - Symlink the `creep` file into your `$PATH`

### Installation for Windows
 - Clone this repo or download a release on the releases page
   - Take note of the path where you installed the `creep` files
 - Edit your environment variables to add the install directory to the `Path`
   - From start menu, search for "environment variables" to find the item "Edit the system environment variables"
   - From the window that opens, click the button "Environment Variables..."
   - Find the Variable "Path" and click the "Edit..." button
   - Change the value to add the full path where you installed the creep files (add it after the last ;)
   - Click OK, OK, OK
 - Now from a command line you should be able to type `creep` and can use the creep commands

## Usage

 - `creep list` - will list all the known packages (mods) in the repository
 - `creep install <package>` - will install the package to your `~/.minecraft/mods` folder
 - `creep uninstall <package>` - will remove the package from your mods folder

The mod files are stored in a cache directory in `~/.creep/cache`

## Future Plans

 - Support dependencies
 - Have a registry where people can define their mods
 - Support multiple versions of a single mod
 - Ability search the registry for mods by typing `creep search furnace`
 - Ability to make collections of mods by requiring other mods or packages

Example `mod.json`. A definition file in json format of a package (mod)
```
{
  "name": "thefrogmc/better-furnaces",
  "version": "4.3",
  "description": "Adds some new furnaces to the game",
  "keywords": "iron furnace, gold furnace, diamond furnace, hell furnace, extreme furnace",
  "require": {
    "minecraft": "1.7.10",
    "forge": "*"
  },
  "filename": "[1.7.10]Better_Furnaces_V4.3.jar",
  "author": "TheFrogMC",
  "homepage": "http://www.minecraftforum.net/forums/mapping-and-modding/minecraft-mods/1279439-better-furnaces-mod"
}   
```
