import logging
from typing import TYPE_CHECKING


logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from telegram import Update, Bot
    from telegram.ext import CallbackContext


def channel_setup(update: 'Update', context: 'CallbackContext'):
    logger.info(f'join chat {update.chat_member.chat.full_name}')
