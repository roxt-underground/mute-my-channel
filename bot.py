#!/usr/bin/env python3
import logging
import os
from datetime import timedelta, time

import pytz
from telegram.ext import Updater, CommandHandler, Dispatcher, Filters

from handlers.mute import (mute_command, unmute_command, mute_delay_command, watch_channel_command,
                           forget_channel_command)
from jobs.dump import dump_job, restore_job
from jobs.mute import mute_attention_job, mute_job, unmute_job


TIME_ZONE = pytz.timezone('Europe/Moscow')

MUTE_ATTENTION_TIME = time(21, 0, 0, tzinfo=TIME_ZONE)
MUTE_START_TIME = time(21, 5, 0, tzinfo=TIME_ZONE)
MUTE_END_TIME = time(9, 0, 0, tzinfo=TIME_ZONE)


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
    dispatcher.add_handler(CommandHandler("watch", watch_channel_command,
                                          filters=(Filters.chat_type.channel | Filters.chat_type.groups)
                                          ))
    dispatcher.add_handler(CommandHandler("forget", forget_channel_command,
                                          filters=(Filters.chat_type.channel | Filters.chat_type.groups)
                                          ))
    dispatcher.add_handler(CommandHandler("mute", mute_command))
    dispatcher.add_handler(CommandHandler("unmute", unmute_command))
    dispatcher.add_handler(CommandHandler('delayed', mute_delay_command))

    # Чтоб не прикручивать базу данных, пока запоминаем всё в файл
    dispatcher.job_queue.run_once(
        restore_job,
        timedelta(0),
    )
    dispatcher.job_queue.run_repeating(
        dump_job,
        timedelta(seconds=20),
        first=timedelta(seconds=20)
    )

    # Таски на управление каналом
    dispatcher.job_queue.run_daily(
        mute_attention_job,
        MUTE_ATTENTION_TIME,
        days=(0, 1, 2, 3, 4, 5, 6),
    )
    dispatcher.job_queue.run_daily(
        mute_job,
        MUTE_START_TIME,
        days=(0, 1, 2, 3, 4, 5, 6),
    )
    dispatcher.job_queue.run_daily(
        unmute_job,
        MUTE_END_TIME,
        days=(0, 1, 2, 3, 4, 5, 6),
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
