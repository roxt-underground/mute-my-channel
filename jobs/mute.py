import logging
from typing import TYPE_CHECKING
from telegram import ChatPermissions

from handlers.mute import set_permissions


CLOSING_ATTENTION_MESSAGE = 'Через 5 минут канал будет закрыт'
CLOSING_SUCCESS_MESSAGE = 'До завтра! Чат будет открыт в 9 утра'
OPEN_SUCCESS_MESSAGE = 'Доброе утро, чат открыт к обсуждениям!'


if TYPE_CHECKING:
    from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


def mute_job(context: 'CallbackContext'):
    bot = context.bot
    permissions = ChatPermissions(
        can_send_messages=False,
        can_change_info=False,
        can_pin_messages=False,
    )

    for chat_id in context.bot_data['channels']:
        set_permissions(
            bot,
            chat_id,
            permissions,
            CLOSING_SUCCESS_MESSAGE,
            None,
        )


def mute_attention_job(context: 'CallbackContext'):
    """Закрывающее сообщение"""
    bot = context.bot
    for chat_id in context.bot_data['channels']:
        logger.info(f'{chat_id} attention')
        bot.send_message(chat_id, CLOSING_ATTENTION_MESSAGE, disable_notification=True)


def unmute_job(context: 'CallbackContext'):
    bot = context.bot
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
    )

    for chat_id in context.bot_data['channels']:
        set_permissions(
            bot,
            chat_id,
            permissions,
            OPEN_SUCCESS_MESSAGE,
            None,
        )
