#!/usr/bin/env python3
import logging
import os

from telegram.ext import Updater, CommandHandler, Dispatcher, ChatMemberHandler

from handlers.chat_join import channel_setup
from handlers.mute import mute_command, unmute_command, mute_delay_command


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('core')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise SystemExit(-1, 'BOT_TOKEN not set in env')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    logger.info('Login success')

    dispatcher: Dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("mute", mute_command))
    dispatcher.add_handler(CommandHandler("unmute", unmute_command))
    dispatcher.add_handler(CommandHandler('delayed', mute_delay_command))

    dispatcher.add_handler(ChatMemberHandler(channel_setup))

    # dispatcher.job_queue.run_repeating(
    #     mute_job,
    #     timedelta(seconds=20),
    # )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
