"""Administration tools for CicloPiBot."""

# Standard library modules
import asyncio
import datetime


async def _restart_command(bot, update, user_record):
    with bot.db as db:
        db['restart_messages'].insert(
            dict(
                text="<i>Restart was successful.</i>",
                chat_id=update['chat']['id'],
                parse_mode='HTML',
                reply_to_message_id=update['message_id'],
                sent=None
            )
        )
    await bot.reply(
        update=update,
        text="I bot verranno riavviati in pochi secondi, caricando prima le "
             "eventuali modifiche al codice."
    )
    bot.__class__.stop(message='=== RESTART ===', final_state=65)
    return


def init(bot):
    """Assign commands to `bot`."""
    @bot.command(command='/restart', aliases=[], show_in_keyboard=False,
                 description="Riavvia i bot",
                 authorization_level='admin')
    async def restart_command(bot, update, user_record):
        return await _restart_command(bot, update, user_record)

    @bot.additional_task('BEFORE')
    async def load_handovers():
        """Perform handovers before running."""
        with bot.db as db:
            for restart_message in db['restart_messages'].find(sent=None):
                asyncio.ensure_future(
                    bot.send_message(
                        **{
                            key: val
                            for key, val in restart_message.items()
                            if key in (
                                'chat_id',
                                'text',
                                'parse_mode',
                                'reply_to_message_id'
                            )
                        }
                    )
                )
                db['restart_messages'].update(
                    dict(
                        sent=datetime.datetime.now(),
                        id=restart_message['id']
                    ),
                    ['id'],
                    ensure=True
                )
        return
