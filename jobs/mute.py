import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # from telegram import Update, Bot
    from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


def mute_job(context: 'CallbackContext'):
    # channels_count = context.user_data
    # logger.info(f'Bot has {channels_count}')
    pass
