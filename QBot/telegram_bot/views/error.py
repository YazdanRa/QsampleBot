from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    Filters,
    MessageHandler,
)
from .start import reply_keyboard


def wrong_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, ("invalid option"))
    return


def cancel(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id,
        text="cancel",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return ConversationHandler.END
