from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    Filters,
    MessageHandler,
)
from .start import reply_keyboard
from .error import error, cancel, wrong_message
from ..models import TelegramUser

BASE = 0


def logging_in(update: Update, context: CallbackContext):

    reply_keyboard = [["with Telegram account", "custom login"], ["Cancel"]]
    chat_id = update.message.from_user.id
    context.bot.send_message(
        chat_id,
        text="options:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return BASE


def default_login(update: Update, context: CallbackContext):
    chat_id = update.message.from_user.id
    if TelegramUser.objects.get(chat_id=chat_id) != None:
        context.user_data["authenticate"] = True
        text = "successfully login"
    else:
        text = "not signed up yet"
    context.bot.send_message(
        chat_id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


def custom_login(update: Update, context: CallbackContext):

    chat_id = update.message.from_user.id
    context.bot.send_message(
        chat_id,
        text="on development",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r"(Login)"), logging_in)],
    states={
        BASE: [
            MessageHandler(Filters.regex(r"(with Telegram account)"), default_login),
            MessageHandler(Filters.regex(r"(custom login)"), custom_login),
        ],
    },
    fallbacks=[
        MessageHandler(Filters.text, wrong_message),
        MessageHandler(Filters.text("Cancel"), cancel),
        MessageHandler(Filters.all, error),
    ],
)
