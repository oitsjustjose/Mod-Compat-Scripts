# Mod Compat Utilities

This library is filled with Python packages that are useful in order to get you up and running with inter-mod compatability within a Vanilla datapack. The datapack you produce using the files output (into `./out/**/*.json`) can be loaded into every world you play using the [Global Resource and Datapacks Mod](https://www.curseforge.com/minecraft/mc-mods/drp-global-datapack).

## Setup

Setup for this is pretty straight forward.

1. Install Python for your current OS: https://www.python.org/downloads/
2. Download this repo by clicking the Green "Clone" button above and choosing `Download Zip`
3. Run the Shell/Batch file (Batch for Windows, Shell for Linux/MacOS/WSL/Other) that corresponds to the data you wish to create (i.e. if I was on Windows wanting to create a set of recipes to turn 2 slabs into their solid-block counterpart, I'd run `./scripts/batch/slabs.bat` by double-clicking it.)
4. Copy the output of `./out` to inside your datapack!

## Usage

To get started with CraftDumper, install it into your modpack and run (as an operator) `/craftdumper blocks data`. You should see in the root of your Minecraft instance a folder named `craftdumper`. Take the CSV (named `blocks_{YYYY-MM-DD_HH-MM-SS}`) and slap it in the root of this repository (which you've presumably cloned). Once you've done that, run any of the scripts (be it Batch or Shell) to create your compatability Datapacks in the `./out` directory.
