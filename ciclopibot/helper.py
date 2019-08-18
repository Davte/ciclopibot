"""Make a self-consistent bot help section."""

# Third party modules
import davtelepot.helper
from davtelepot.utilities import json_read

# Project modules
from .messages import default_help_messages


def init(bot, help_messages=None,
         help_buttons=[]):
    """Assign parsers, commands, buttons and queries to given `bot`."""
    if help_messages is None:
        help_messages = default_help_messages
    davtelepot.helper.init(
        bot=bot,
        help_messages=help_messages,
    )
