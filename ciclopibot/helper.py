"""Make a self-consistent bot help section."""

# Third party modules
from davtelepot.utilities import (
    extract, get_cleaned_text, json_read, make_inline_keyboard,
    make_lines_of_buttons, make_button, MyOD
)

DENY_MESSAGE = (
    "Chiedi di essere autorizzato: se la tua richiesta verrà accolta, "
    "ripeti il comando /help per leggere il messaggio di aiuto."
)


def get_command_description(bot, update, user_record):
    """Get a string description of `bot` commands.

    Show only commands available for `update` sender.
    """
    user_role = bot.Role.get_user_role(
        user_record=user_record
    )
    return "\n".join(
        [
            "/{}: {}".format(
                command,
                details['description']
            )
            for command, details in sorted(
                bot.commands.items(),
                key=lambda x:x[0]
                )
            if details['description']
            and user_role.code <= bot.Role.get_user_role(
                user_role_id=details['authorization_level']
            ).code
        ]
    )


def _make_button(x, y):
    if not y.startswith('help:///'):
        y = 'help:///{}'.format(y)
    return make_button(x, y)


HELP_MENU_BUTTON = make_inline_keyboard(
    [
        _make_button(
            'Torna al menu Guida 📖',
            'menu'
        )
    ],
    1
)


def get_help_buttons(bot, update, user_record):
    """Get `bot` help menu inline keyboard.

    Show only buttons available for `update` sender.
    """
    user_role = bot.Role.get_user_role(
        user_record=user_record
    )
    buttons_list = [
        _make_button(
            section['label'],
            section['abbr']
        )
        for section in bot.help_sections.values()
        if 'auth' in section
        and user_role.code <= bot.Role.get_user_role(
            user_role_id=section['auth']
        ).code
    ]
    return dict(
        inline_keyboard=(
            make_lines_of_buttons(buttons_list, 3)
            + make_lines_of_buttons(
                [
                    _make_button('Comandi 🤖', 'commands')
                ],
                1
            )
            + (
                bot.help_buttons
                if bot.authorization_function(update=update,
                                              authorization_level='user')
                else []
            )
        )
    )


async def _help_command(bot, update, user_record):
    if not bot.authorization_function(update=update,
                                      authorization_level='everybody'):
        return DENY_MESSAGE
    reply_markup = get_help_buttons(bot, update, user_record)
    return dict(
        text=bot.help_message.format(bot=bot),
        parse_mode='HTML',
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


async def _help_button(bot, update, user_record):
    data = update['data']
    command = extract(data, ':///')
    result, text, rm = '', '', None
    if command == 'commands':
        text = "<b>Comandi di {bot.name}</b>\n\n{cd}".format(
            bot=bot,
            cd=get_command_description(bot, update, user_record)
        )
        rm = HELP_MENU_BUTTON
    elif command == 'menu':
        text = bot.help_message.format(bot=bot)
        rm = get_help_buttons(bot, update, user_record)
    else:
        for code, section in bot.help_sections.items():
            if section['abbr'] == command:
                if not bot.authorization_function(
                    update=update,
                    authorization_level=section['auth']
                ):
                    return "Non sei autorizzato!"
                rm = HELP_MENU_BUTTON
                text = (
                    '<b>{s[label]}</b>\n\n{s[descr]}'
                ).format(
                    s=section
                ).format(
                    bot=bot
                )
                break
    if text or rm:
        return dict(
            text=result,
            edit=dict(
                text=text,
                parse_mode='HTML',
                reply_markup=rm,
                disable_web_page_preview=True
            )
        )
    return result


async def _start_command(bot, update, user_record):
    text = get_cleaned_text(update=update, bot=bot, replace=['start'])
    if not text:
        return await _help_command(bot, update, user_record)
    update['text'] = text
    await bot.text_message_handler(
        update=update,
        user_record=None
    )
    return


def init(bot, help_message="<b>Guida</b>",
         help_sections_file='data/help.json', help_buttons=[]):
    """Assign parsers, commands, buttons and queries to given `bot`."""
    bot.help_message = help_message
    bot.help_buttons = help_buttons
    bot.help_sections = MyOD()
    for code, section in enumerate(
        json_read(
            help_sections_file,
            default=[]
        )
    ):
        bot.help_sections[code] = section

    @bot.command("/start", authorization_level='everybody')
    async def start_command(bot, update, user_record):
        return await _start_command(bot, update, user_record)

    @bot.command(command='/help', aliases=['Guida 📖', '00help'],
                 show_in_keyboard=True, description="Aiuto",
                 authorization_level='everybody')
    async def help_command(bot, update, user_record):
        result = await _help_command(bot, update, user_record)
        return result

    @bot.button(prefix='help:///', authorization_level='everybody')
    async def help_button(bot, update, user_record):
        return await _help_button(bot, update, user_record)
