#!/bin/bash

# This file must be executable, otherwise the service cannot run it.

# Run `$python_script` while exit code is 65.
# At each iteration, pull news from repository and update dependencies.

# Get current directory
this_script_directory=$(cd `dirname $0` && pwd)

# Import variables from my_config.sh
#  `$python_virtual_environment`: python virtual environment directory
#    containing `python` and `pip`
# `$python_script`: complete path to python script to be run
source $this_script_directory/my_config.sh;

# Ensure the success of importing procedure:
## variables of interest should be non-zero (`-z`)
if [ -z ${python_virtual_environment} ];
then
  printf "Please set in \"my_config.sh\" the path to bot python \
virtual environment\n\
\n\
Example:\n\
python_virtual_environment=\"path/to/virtual/env\"\n\
";
  exit;
fi
if [ -z ${python_script} ];
then
  printf "Please set in \"my_config.sh\" the path to python script to be run \
\n\
Example:\n\
python_script=\"path/to/python/script.py\"\n\
";
  exit;
elif [ ! -e ${python_script} ];
then
  printf "File $python_script does not exist\n\
Please point to a valid file.\n\
Example:\n\
python_script=\"path/to/python/script.py\"\n\
";
fi

echo "Python script will be run while it exits with value===65.";
i=65;
while [ $i -eq 65 ]
do
  echo "Pulling from repository..."
  git pull;
  echo "Updating dependencies";
  $python_virtual_environment/pip install --upgrade --no-cache-dir \
  --no-deps davtelepot;
  echo "Running python script";
  $python_virtual_environment/python -m ciclopibot.bot;
  i=$?;
done
