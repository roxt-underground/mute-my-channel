import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Union
from telegram import ChatPermissions
from telegram.error import BadRequest


logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from telegram import Update, Bot
    from telegram.ext import CallbackContext


def mute_command(update: 'Update', context: 'CallbackContext') -> None:
    """mute channel for simple users"""
    permissions = ChatPermissions(
        can_send_messages=False,
        can_change_info=False,
        can_pin_messages=False,
    )
    _set_permissions(context.bot, update.message.chat.id, permissions, 'Чат закрыт для новых сообщений')


def unmute_command(update: 'Update', context: 'CallbackContext') -> None:
    """unmute channel"""
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
    )
    _set_permissions(context.bot, update.message.chat.id, permissions, 'Можете продолжить общение!')


def mute_delay_command(update: 'Update', context: 'CallbackContext'):
    permissions = ChatPermissions(
        can_send_messages=False,
        can_change_info=False,
        can_pin_messages=False,
    )
    context.job_queue.run_once(lambda _context: _set_permissions(
        _context.bot,
        update.message.chat.id,
        permissions,
        'Время вышло, до свидания!'
    ), timedelta(seconds=30))
    update.message.chat.send_message('Чат закроется через 30 секунд')


def _set_permissions(
        bot: 'Bot',
        chat_id: int,
        permissions: ChatPermissions,
        success_message: Union[str, None] = None,
        error_message: Union[str, None] = 'У бота недостаточно прав',
):
    try:
        bot.set_chat_permissions(
            chat_id,
            permissions
        )
    except BadRequest as e:
        logger.warning(f'permission set error: {e}')
        bot.send_message(chat_id, error_message)
    else:
        if success_message:
            bot.send_message(chat_id, success_message)
