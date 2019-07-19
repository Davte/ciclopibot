"""Provide bike sharing information via Telegram bot."""

# Standard library modules
import logging
import os
import sys

# Third party modules
from davtelepot.bot import Bot

# Project modules
from . import bot_tools
from . import ciclopi
from . import helper
from . import roles
from .data.passwords import bot_token

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
    bot.set_unknown_command_message(
        "Comando sconosciuto!\n"
        "Scrivi /help per visualizzare la guida."
    )
    bot.set_authorization_function(
        roles.get_authorization_function(bot)
    )
    bot.set_authorization_denied_message(
        "Non disponi di autorizzazioni sufficienti per questo comando."
    )
    with bot.db as db:
        db['users'].upsert(
            dict(
                telegram_id=63538990,
                privileges=1
            ),
            ['telegram_id']
        )
    bot_tools.init(bot)
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
    roles.init(bot)
    # Run bot(s)
    logging.info("Presso ctrl+C to exit.")
    exit_state = Bot.run(
        local_host=local_host,
        port=port
    )
    sys.exit(exit_state)
