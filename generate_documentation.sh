#!/bin/bash

# Get current directory
this_script_directory=$(cd `dirname $0` && pwd)

# Import variables from my_config.sh
#  `$python_virtual_environment`: python virtual environment directory for packaging
#    containing `python` and `pip`
source "$this_script_directory/my_config.sh";

# Ensure the success of importing procedure
if [ -z "${python_virtual_environment}" ];
then
  printf "Please set in ""my_config.sh"" the path to bot python virtual environment\n\nExample:\npython_virtual_environment=""path/to/virtual/env""\n";
  exit;
fi

"$python_virtual_environment/python" -m pdoc --html --force --output "$this_script_directory/temp" "$this_script_directory/ciclopibot";

rm -rf documentation/;

mv "$this_script_directory/temp/ciclopibot/" "$this_script_directory/documentation/";

rm -rf temp/;
