from typing import TYPE_CHECKING
from telegram import Update, ChatPermissions
from telegram.error import BadRequest


if TYPE_CHECKING:
    from telegram.ext import CallbackContext


def mute_command(update: Update, context: 'CallbackContext') -> None:
    """mute channel for simple users"""
    members_count = update.message.chat.get_member_count()
    update.message.reply_text('\n'.join([
        f'На канале {members_count} участников(а)',
    ]))
    permissions = ChatPermissions(
        can_send_messages=False,
        can_change_info=False,
        can_pin_messages=False,
    )

    try:
        context.bot.set_chat_permissions(
            update.message.chat.id,
            permissions
        )
    except BadRequest:
        update.message.reply_text('У бота недостаточно прав')


def unmute_command(update: Update, context: 'CallbackContext') -> None:
    """unmute channel"""
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
    )
    try:
        context.bot.set_chat_permissions(
            update.message.chat.id,
            permissions
        )
    except BadRequest:
        update.message.reply_text('У бота недостаточно прав')

