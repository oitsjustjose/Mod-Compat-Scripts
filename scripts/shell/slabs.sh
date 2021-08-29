#!/bin/bash

### BOILERPLATE: DETECTING PYTHON ###

PYTHON=$(which python)
if [ $? -eq 1 ]
then
    PYTHON=$(which python3)
    if [ $? -eq 1 ]
    then
        printf "\e[31mCould not determine Python[3] path - is it installed?\e[39m"
        exit
    fi
fi

### BOILERPLATE: DETECTING PIP ###

PIP=$(which pip)
if [ $? -eq 1 ]
then
    PYTHON=$(which pip3)
    if [ $? -eq 1 ]
    then
        printf "\e[31mCould not determine Pip[3] path - is it installed?\e[39m"
        exit
    fi
fi

### BOILERPLATE: INSTALLING DEPS ###

printf "\e[95mInstalling prerequisites... \e[39m"
cd "$(pwd)/../.." 
$PIP install -q -r requirements.txt;
printf "\e[32mDone!\e[39m\n"

### END BOILERPLATE! ###

# Make user wait to validate that they have everything ready.
printf "\e[93mFor this script to work, an export of Blocks (data) from CraftDumper
    (https://dv2ls.com/craftdumper) must be in the root of this directory.\e[39m\n"
read -rsn1 -p"If it is not, do so now before pressing any key...";echo

printf "\n\n\n"

$PYTHON -m src.modules.slab_to_block;