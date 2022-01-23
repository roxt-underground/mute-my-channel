import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Union
from telegram import ChatPermissions, ChatMember
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
    if not is_admin(update):
        update.message.reply_text('У вас недостаточно прав.')
        return

    set_permissions(context.bot, update.message.chat.id, permissions, 'Чат закрыт для новых сообщений')


def unmute_command(update: 'Update', context: 'CallbackContext') -> None:
    """unmute channel"""
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
    )
    if not is_admin(update):
        update.message.reply_text('У вас недостаточно прав.')
        return

    set_permissions(context.bot, update.message.chat.id, permissions, 'Можете продолжить общение!')


def mute_delay_command(update: 'Update', context: 'CallbackContext'):
    permissions = ChatPermissions(
        can_send_messages=False,
        can_change_info=False,
        can_pin_messages=False,
    )
    context.job_queue.run_once(lambda _context: set_permissions(
        _context.bot,
        update.message.chat.id,
        permissions,
        'Время вышло, до свидания!'
    ), timedelta(seconds=30))
    update.message.chat.send_message('Чат закроется через 30 секунд')


def watch_channel_command(update: 'Update', context: 'CallbackContext'):
    channels = get_channels(context)
    chat_id = update.message.chat_id

    if not is_admin(update):
        update.message.reply_text('У вас недостаточно прав.')
        return

    if chat_id in channels:
        update.message.reply_text('Я уже слежу за этим чатом.')
    else:
        channels.append(chat_id)
        update.message.reply_text('Хорошо! Чат под моим контролем.')


def forget_channel_command(update: 'Update', context: 'CallbackContext'):
    channels = get_channels(context)
    chat_id = update.message.chat_id

    if not is_admin(update):
        update.message.reply_text('У вас недостаточно прав.')
        return

    if chat_id in channels:
        channels.pop(channels.index(chat_id))
        update.message.chat.send_message('Тут больше нет моей власти.')
    else:
        update.message.reply_text('Мне этот канал не знаком')


def is_admin(update: 'Update') -> bool:
    sender_id = update.message.from_user.id
    return update.message.chat.get_member(sender_id).status in (ChatMember.ADMINISTRATOR, ChatMember.CREATOR)


def get_channels(context: 'CallbackContext'):
    context.bot_data.setdefault('channels', [])
    channels: list = context.bot_data['channels']
    return channels


def set_permissions(
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
