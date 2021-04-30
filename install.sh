#!/bin/bash

# Get current directory
this_script_directory=$(cd "$(dirname "$0")" && pwd);
cd "$this_script_directory" || exit 1;
configuration_file="$this_script_directory/my_config.sh";
passwords_file="$this_script_directory/ciclopibot/data/passwords.py";

# Create intermediate path for passwords_file, if it does not exist
mkdir -p "$this_script_directory/ciclopibot/data/";

echo "Enter a name for your virtual environment";
read venv_name;
python3 -m venv "$venv_name";
"$venv_name"/bin/pip install -r "$this_script_directory/requirements.txt";

# Please note that this will work only in a Unix-like operating system.
# Other systems may require a different path.
echo "python_virtual_environment=\"$(pwd)/$venv_name/bin\";" >> "$configuration_file";
echo "python_script=\"$this_script_directory/ciclopibot/bot.py\";" >> "$configuration_file";
read -r "Enter a valid Telegram bot token           " bot_token;
echo "bot_token = \"$bot_token\"" >> "$passwords_file";

# Run bot
bash run_me.sh;
