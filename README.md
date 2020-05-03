# CicloPiBot
[@CicloPiBot](https://t.me/ciclopibot) is a Telegram bot based on [davtelepot](https://gogs.davte.it/davte/davtelepot) which provides information about CicloPi, the public bike-sharing service in Pisa.

## Usage
### Client side
Send [`/start`](https://t.me/ciclopibot?start=00help) [@CicloPiBot](https://t.me/ciclopibot), all you need is a [Telegram account](https://telegram.org/).

**Commands**
* `/start` the bot
* Ask for `/help` for further information
* Ask for `/ciclopi` information

### "Server" side
You may choose between method 1 (`pip`) and method 2 (`git`).
1. Using `pip`
    * Install ciclopibot
    ```bash
    pip install ciclopibot
   ``` 
   * Run ciclopibot as module
   ```bash
   python -m ciclopibot -h  # Get help 
   python -m ciclopibot <your_token_here>
   ```
1. Using `git`
    * Clone this repository
    ```bash
    git clone ssh://git@gogs.davte.it:8445/Davte/ciclopibot.git
    # git clone https://gogs.davte.it/Davte/ciclopibot.git
    # git clone git@github.com:Davte/ciclopibot.git
    # git clone https://github.com/Davte/ciclopibot.git
    ```
    * Run `install.sh`: it will help you perform the following operations.
      * Put a Telegram bot token in gitignored `data/passwords.py` module.
        * To get a token, ask [@BotFather](https://t.me/botfather).
        * The bot whose token you use will act as [@CicloPiBot](https://t.me/ciclopibot) as long as you run the script.
      * Create a python3.5+ virtual environment and install requirements.
      * Specify `python_virtual_environment` and `python_script` variables in `my_config.sh`
    * Run `run_me.sh`
    ```bash
    bash run_me.sh;
    ```
    * You may edit the file and test your code with your bot.
    * Should you be satisfied of your edits enough, you may fork this repository and open a pull request.

## Credits
* [Davte](https://www.davte.it) is the creator and the main author of this repository.
* All data are obtained from [CicloPi website](http://www.ciclopi.eu) and are meant to help users save time when using their service. Misuse is discouraged.
* [Minala](https://t.me/minalabot) inspired the idea and gave a first version of this service many years ago with a different implementation.
