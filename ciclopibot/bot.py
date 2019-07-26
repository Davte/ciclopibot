"""Provide bike sharing information via Telegram bot."""

# Standard library modules
import logging
import os
import sys

# Third party modules
import davtelepot
from davtelepot import administration_tools, authorization, languages

# Project modules
from . import ciclopi
from . import helper
from .data.passwords import bot_token

language_messages = {
    'language_command': {
        'name': {
            'en': "/language",
            'it': "/lingua"
        },
        'alias': {
            'en': "Language 🗣",
            'it': "Lingua 🗣"
        },
        'description': {
            'en': "Change language settings",
            'it': "Cambia le impostazioni della lingua"
        }
    },
    'language_button': {
        'description': {
            'en': "Change language settings",
            'it': "Cambia le impostazioni della lingua"
        }
    },
    'language_panel': {
        'text': {
            'en': "<b>Choose a language</b>",
            'it': "<b>Seleziona una lingua</b>"
        }
    }
}

supported_languages = {
    'en': {
        'flag': '🇬🇧',
        'name': 'English'
    },
    'it': {
        'flag': '🇮🇹',
        'name': 'Italiano'
    }
}

ciclopibot_help_messages = {
    'help_command': {
        'text': {
                'en': "<b>📖 {bot.name} guide</b>\n\n"
                      "Welcome!\n"
                      "To visit a guide section, press the corresponding "
                      "button.\n"
                      "To view all available commands, see section "
                      "`Comandi`.\n\n"
                      "Bot author and administrator: @Davte",
                'it': "<b>📖 Guida di {bot.name}\n\n</b>"
                      "Benvenuto!\n"
                      "Per leggere una sezione della guida premi il bottone "
                      "corrispondente. Per conoscere  tutti i comandi "
                      "disponibili, visita l'apposita sezione della guida "
                      "premendo il pulsante Comandi.\n\n"
                      "Autore e amministratore del bot: @Davte"
            },
        'description': {
            'en': "Help",
            'it': "Aiuto"
        }
    }
}


if __name__ == '__main__':
    path = os.path.dirname(__file__)
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
    administration_tools.init(bot)
    ciclopi.init(bot)
    helper.init(
        bot=bot,
        help_messages=ciclopibot_help_messages,
        help_sections_file='ciclopibot/data/help.json'
    )
    authorization.init(bot)
    languages.init(
        bot, language_messages=language_messages,
        supported_languages=supported_languages
    )
    # Run bot(s)
    logging.info("Press ctrl+C to exit.")
    exit_state = davtelepot.bot.Bot.run(
        local_host=local_host,
        port=port
    )
    sys.exit(exit_state)
