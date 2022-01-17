"""
На текущем этапе я хочу заморачиваться с базами данных, по этому я буду просто делать дамп состояния бота в json
"""
import json
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # from telegram import Update, Bot
    from telegram.ext import CallbackContext


def dump_job(context: 'CallbackContext'):
    with open('state.json', 'w') as state_file:
        json.dump(context.bot_data, state_file, indent=2, ensure_ascii=False, sort_keys=True)


def restore_job(context: 'CallbackContext'):
    with open('state.json', 'r') as state_file:
        data = json.load(state_file)
        context.bot_data.update(data)
