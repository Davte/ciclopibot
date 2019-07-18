"""Provide bike sharing information via Telegram bot."""

# Standard library modules
import logging
import os

# Third party modules
from davtelepot.bot import Bot

# Project modules
import ciclopi
from data.passwords import bot_token
import helper

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    try:
        from data.config import log_file_name
    except ImportError:
        log_file_name = 'CicloPi.info.log'
    try:
        from data.config import errors_file_name
    except ImportError:
        errors_file_name = 'CicloPi.errors.log'
    try:
        from data.config import local_host, port
    except ImportError:
        local_host, port = '127.0.0.1', 3000
    log_file = f"{path}/data/{log_file_name}"
    errors_file = f"{path}/data/{errors_file_name}"

    # Outputs the log in console, log_file and errors_file
    # Log formatter: datetime, module name (filled with spaces up to 15
    # characters), logging level name (filled to 8), message
    log_formatter = logging.Formatter(
        "%(asctime)s [%(module)-15s %(levelname)-8s]     %(message)s",
        style='%'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    file_handler = logging.FileHandler(errors_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_formatter)
    consoleHandler.setLevel(logging.DEBUG)
    root_logger.addHandler(consoleHandler)

    # Instantiate bot
    bot = Bot(token=bot_token, database_url='ciclopibot/data/ciclopi.db')
    # Assign commands to bot
    ciclopi.init(bot)
    helper.init(
        bot=bot,
        help_message="<b>📖 Guida di {bot.name}\n\n</b>"
                     "Benvenuto!\n"
                     "Per conoscere i comandi disponibili visita l'apposita "
                     "sezione della guida premendo il pulsante Comandi.\n\n"
                     "Autore e amministratore del bot: @davte",
        help_sections_file='ciclopibot/data/help.json'
    )
    # Run bot(s)
    logging.info("Presso ctrl+C to exit.")
    Bot.run(
        local_host=local_host,
        port=port
    )
