"""Provide bike sharing information via Telegram bot."""

# Standard library modules
import logging
import os
import sys

# Third party modules
import davtelepot

# Project modules
from . import ciclopi
from .data.passwords import bot_token
from .messages import (
    default_help_messages, language_messages, supported_languages
)

if __name__ == '__main__':
    path = os.path.dirname(
        os.path.abspath(
            __file__
        )
    )
    try:
        from .data.config import log_file_name
    except ImportError:
        log_file_name = 'CicloPi.info.log'
    try:
        from .data.config import errors_file_name
    except ImportError:
        errors_file_name = 'CicloPi.errors.log'
    try:
        from .data.config import local_host, port
    except ImportError:
        local_host, port = '127.0.0.1', 3000
    try:
        from .data.config import hostname, certificate
    except ImportError:
        hostname, certificate = '', None
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
    bot = davtelepot.bot.Bot(token=bot_token,
                             database_url=f'{path}/data/ciclopi.db',
                             hostname=hostname, certificate=certificate)
    bot.set_path(path)
    bot.set_class_log_file_name(log_file_name)
    bot.set_class_errors_file_name(errors_file_name)
    bot.set_unknown_command_message(
        "Comando sconosciuto!\n"
        "Scrivi /help per visualizzare la guida."
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
    davtelepot.administration_tools.init(bot)
    ciclopi.init(bot)
    davtelepot.authorization.init(bot)
    davtelepot.languages.init(
        bot, language_messages=language_messages,
        supported_languages=supported_languages
    )
    davtelepot.suggestions.init(bot)
    davtelepot.helper.init(bot, help_messages=default_help_messages)
    # Run bot(s)
    logging.info("Press ctrl+C to exit.")
    exit_state = davtelepot.bot.Bot.run(
        local_host=local_host,
        port=port
    )
    sys.exit(exit_state)
