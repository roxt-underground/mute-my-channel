from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext


def echo(update: 'Update', context: 'CallbackContext') -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text[::-1])
