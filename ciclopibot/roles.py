"""Handle authorization-related functions."""

# Standard library modules
import datetime
import json

# Third party modules
from davtelepot.utilities import (
    Confirmator, extract, get_cleaned_text, make_button, make_inline_keyboard,
    MyOD
)

ROLES = MyOD()
ROLES[0] = {'abbr': 'banned',
            'symbol': '🚫',
            'plural': 'bannati',
            'singular': 'bannato',
            'can_appoint': [],
            'can_be_appointed': [1, 2, 3]
            }
ROLES[1] = {'abbr': 'founder',
            'symbol': '👑',
            'plural': 'fondatori',
            'singular': 'fondatore',
            'can_appoint': [0, 1, 2, 3, 4, 5, 7, 100],
            'can_be_appointed': []
            }
ROLES[2] = {'abbr': 'admin',
            'symbol': '⚜️',
            'plural': 'amministratori',
            'singular': 'amministratore',
            'can_appoint': [0, 3, 4, 5, 7, 100],
            'can_be_appointed': [1]
            }
ROLES[3] = {'abbr': 'moderator',
            'symbol': '🔰',
            'plural': 'moderatori',
            'singular': 'moderatore',
            'can_appoint': [0, 5, 7],
            'can_be_appointed': [1, 2]
            }
ROLES[5] = {'abbr': 'user',
            'symbol': '🎫',
            'plural': 'utenti registrati',
            'singular': 'utente registrato',
            'can_appoint': [],
            'can_be_appointed': [1, 2, 3]
            }
ROLES[100] = {'abbr': 'everybody',
              'symbol': '👤',
              'plural': 'chiunque',
              'singular': 'chiunque',
              'can_appoint': [],
              'can_be_appointed': [1, 2, 3]
              }


def _get_user_role_panel(user_record):
    text = """👤 <a href="tg://user?id={u[telegram_id]}">{u[username]}</a>
🔑 <i>{r}</i> {s}
    """.format(
        u=user_record,
        r=ROLES[user_record['privileges']]['singular'].capitalize(),
        s=ROLES[user_record['privileges']]['symbol'],
    )
    buttons = [
        make_button(
            '{s} {r}'.format(
                s=role['symbol'],
                r=role['singular'].capitalize()
            ),
            'auth:///set|{a[id]}_{c}'.format(
                c=code,
                a=user_record
            )
        )
        for code, role in ROLES.items()
    ]
    return text, buttons


async def _authorization_command(bot, update, user_record):
    text = get_cleaned_text(bot=bot, update=update, replace=['auth'])
    reply_markup = None
    result = '<code>Caso non previsto :/</code>'
    if not text:
        if 'reply_to_message' not in update:
            result = "Usa questo comando in risposta a un utente registrato "\
                     "(oppure scrivi <code>/auth username</code>) per "\
                     "cambiarne il grado di autorizzazione."
        else:
            with bot.db as db:
                user_record = db['users'].find_one(
                    telegram_id=update['reply_to_message']['from']['id']
                )
            if not user_record:
                result = "Chi ha inviato questo messaggio non è un utente "\
                         "registrato.\nDeve essere lui ad avviare il bot e "\
                         "inviare il comando /askauth\nPotrai allora "\
                         "modificare i suoi permessi rispondendo a un suo "\
                         "messaggio (come hai fatto ora)."
            else:
                result, buttons = _get_user_role_panel(user_record)
                reply_markup = make_inline_keyboard(buttons, 1)
    else:
        with bot.db as db:
            user_record = list(
                db.query(
                    """SELECT *
                    FROM users
                    WHERE username LIKE '{}%'
                    """.format(
                        text
                    )
                )
            )
        if not user_record:
            result = "Utente sconosciuto"
        else:
            user_record = user_record[0]
            result, buttons = _get_user_role_panel(user_record)
            reply_markup = make_inline_keyboard(buttons, 1)
    return dict(
        text=result,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def _ask_for_authorization_command(bot, update, user_record):
    chat_id = update['chat']['id']
    username = (
        update['from']['username']
        if 'username' in update['from']
        else None
    )
    if chat_id < 0:
        return dict(
            chat_id=chat_id,
            text="Passa a una chat privata con @{} per questa funzione. "
                 "Dovrai prima fare /start, se non hai ancora mai "
                 "usato il bot.".format(
                    bot.name
                 )
        )
    user_id = update['from']['id']
    with bot.db as db:
        check = db['users'].find_one(telegram_id=user_id)
        admins = db['users'].find(privileges=[1, 2])
    if check:
        if not check['privileges']:
            return "Sei stato bannato!"
        return "Sei già registrato"
    for admin in admins:
        await bot.send_message(
            chat_id=admin['telegram_id'],
            text="""Vuoi autorizzare il seguente """
                 """<a href="tg://user?id={user}">utente</a>?\n"""
                 """<code>{data}</code>""".format(
                data=json.dumps(
                    update['from'],
                    indent=2
                ),
                user=user_id
            ),
            parse_mode="HTML",
            reply_markup=dict(
                inline_keyboard=[
                    [
                        make_button(
                            "Autorizza",
                            "auth:///auth|{i}_{n}".format(
                                i=user_id,
                                n=username
                            )
                        ),
                        make_button(
                            "Banna",
                            "auth:///ban|{i}_{n}".format(
                                i=user_id,
                                n=username
                            )
                        )
                    ]
                ]
            )
        )
    return "Richiesta di autorizzazione inoltrata."


async def _ban_command(bot, update, user_record):
    chat_id = update['chat']['id']
    if 'reply_to_message' not in update:
        return dict(
            text="Questo comando va usato in risposta",
            chat_id=chat_id
        )
    user_id = update['reply_to_message']['from']['id']
    with bot.db as db:
        record = db['users'].find_one(telegram_id=user_id)
        if record and record['privileges'] == 0:
            return dict(text="Questo utente è già bannato", chat_id=chat_id)
        db['users'].upsert(
            dict(
                telegram_id=user_id,
                privileges=0
            ),
            ['telegram_id']
        )
    return dict(text="Utente bannato.", chat_id=chat_id)


async def _authorization_button(bot, update, user_record):
    data = update['data']
    command = extract(data, ':///', '|')
    arguments = extract(data, "|").split('_')
    user_id = update['from']['id']
    other_user_id = int(arguments[0])
    result, text, reply_markup = '', '', None
    if command in ['auth', 'ban']:
        username = arguments[1]
    if command in ['auth']:
        with bot.db as db:
            record = db['users'].find_one(telegram_id=user_id)
            if record:
                return "Queste utente è già autorizzato."
            db['users'].upsert(
                dict(
                    telegram_id=user_id,
                    privileges=5,
                    username=username
                ),
                ['telegram_id']
            )
        await bot.send_message(
            chat_id=user_id,
            text="Sei stato autorizzato a usare il bot :D Per info: /help"
        )
        result = "Utente autorizzato."
    elif command in ['ban']:
        with bot.db as db:
            record = db['users'].find_one(telegram_id=user_id)
            if record and record['privileges'] == 0:
                return "Questo utente è già bannato"
            db['users'].upsert(
                dict(
                    telegram_id=user_id,
                    privileges=0,
                    username=username
                ),
                ['telegram_id']
            )
        result = "Utente bannato."
    elif command in ['set']:
        other_user_id, other_user_privileges = (int(x) for x in arguments)
        if not Confirmator.get(
            key='{}_set_{}'.format(
                user_id,
                other_user_id
            ),
            confirm_timedelta=5
        ).confirm:
            return "Sicuro sicuro?"
        with bot.db as db:
            user_record = db['users'].find_one(telegram_id=user_id)
            other_user_record = db['users'].find_one(id=other_user_id)
        if other_user_record is None:
            other_user_record = dict(privileges=100)
        if (
            other_user_privileges not in (
                ROLES[user_record['privileges']]['can_appoint']
            )
            or user_record['privileges'] not in (
                ROLES[other_user_record['privileges']]['can_be_appointed']
            )
        ):
            result = "Permesso negato"
            text = "Non hai l'autorità di conferire questo grado di "\
                   "autorizzazione a questo utente!"
            buttons = [
                make_button(
                    'Torna all\'utente',
                    'auth:///show|{}'.format(
                        other_user_id
                    )
                )
            ]
            reply_markup = make_inline_keyboard(buttons, 1)
        else:
            with bot.db as db:
                db['users'].update(
                    dict(
                        id=other_user_id,
                        privileges=other_user_privileges
                    ),
                    ['id']
                )
                other_user_record = db['users'].find_one(id=other_user_id)
            result = "Permesso conferito"
            text, buttons = _get_user_role_panel(other_user_record)
            reply_markup = make_inline_keyboard(buttons, 1)
    elif command in ['show']:
        with bot.db as db:
            other_user_record = db['users'].find_one(id=other_user_id)
        text, buttons = _get_user_role_panel(other_user_record)
        reply_markup = make_inline_keyboard(buttons, 1)
    if text:
        return dict(
            text=result,
            edit=dict(
                text=text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        )
    return result


def init(bot):
    """Assign parsers, commands, buttons and queries to given `bot`."""
    @bot.command(command='/auth', aliases=[], show_in_keyboard=False,
                 description="Cambia il grado di autorizzazione di un utente "
                             "(in risposta o scrivendone l'utenza)",
                 authorization_level='moderator')
    async def authorization_command(bot, update, user_record):
        return await _authorization_command(bot, update, user_record)

    @bot.button('auth:///', authorization_level='admin')
    async def authorization_button(bot, update, user_record):
        return await _authorization_button(bot, update, user_record)

    @bot.command('/ban', description="Banna l'utente (da usare in risposta)",
                 authorization_level='admin')
    async def ban_command(bot, update, user_record):
        return await _ban_command(bot, update, user_record)


def get_privilege_code(privileges):
    """Get privilege code."""
    if not privileges:
        privileges = 'everybody'
    if privileges in [x['abbr'] for x in ROLES.values()]:
        privileges = ROLES.get_by_key_val('abbr', privileges)
    assert type(privileges) is int, ("privileges must be either a ROLES "
                                     "role abbreviation or a ROLES code")
    return privileges


def get_role(bot, update, user_record=None):
    """Get role of `update` sender.

    Update user record as well.
    """
    if type(update) is int:
        user_id = update
        # Mark this update as fake by adding a `notes` field
        update = {'from': {'id': user_id, 'notes': 'Unavailable data'}}
    else:
        user_id = update['from']['id']
    assert type(user_id) is int, "user_id must be a telegram user id, "\
                                 "or an update object sent from it"
    role = 100
    with bot.db as db:
        if user_record is None:
            user_record = db['users'].find_one(
                telegram_id=user_id
            )
        if user_record is None:
            new_user = dict(telegram_id=user_id, privileges=100)
            for key in [
                'first_name',
                'last_name',
                'username',
                'language_code'
            ]:
                new_user[key] = (
                    update['from'][key]
                    if key in update['from']
                    else None
                )
            db['users'].insert(new_user)
            user_record = db['users'].find_one(telegram_id=user_id)
        else:
            new_user = dict()
            for key in [
                'first_name',
                'last_name',
                'username',
                'language_code'
            ]:
                new_user[key] = (
                    update['from'][key]
                    if key in update['from']
                    else None
                )
                if (
                    (
                        key not in user_record
                        or new_user[key] != user_record[key]
                    )
                    and 'notes' not in update['from']  # Exclude fake updates
                ):
                    db['users_history'].insert(
                        dict(
                            until=datetime.datetime.now(),
                            user_id=user_record['id'],
                            field=key,
                            value=(
                                user_record[key]
                                if key in user_record
                                else None
                            )
                        )
                    )
                    db['users'].update(
                        {
                            'id': user_record['id'],
                            key: new_user[key]
                        },
                        ['id'],
                        ensure=True
                    )
    if (
        user_record is not None
        and 'privileges' in user_record
        and user_record['privileges'] is not None
    ):
        role = user_record['privileges']
    return role


def get_authorization_function(bot):
    """Take a bot and return its authorization function."""
    def is_authorized(update, user_record=None, authorization_level=2):
        authorization_level = get_privilege_code(authorization_level)
        # Channel posts will be considered as made by "anyone"
        if (
            isinstance(update, dict)
            and 'from' not in update
        ):
            role = 100
        else:
            role = get_role(bot, update)
        if any([
            not role,
            role > authorization_level
        ]):
            return False
        return True
    return is_authorized
