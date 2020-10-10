from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, Filters, MessageHandler
from .start import reply_keyboard
from .error import error, wrong_message, cancel
from ..models import TelegramUser

BASE = 0


def signing_up(update: Update, context: CallbackContext):

    reply_keyboard = [["with Telegram account", "custom sign up"], ["Cancel"]]
    chat_id = update.message.from_user.id
    context.bot.send_message(
        chat_id,
        text="options:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return BASE


def default_create_user(update: Update, context: CallbackContext):
    try:
        chat_id = update.message.from_user.id
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name or None
        is_bot = update.message.from_user.is_bot
        language_code = update.message.from_user.language_code

        TelegramUser.objects.create(
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_bot=is_bot,
            language_code=language_code,
        )

        text = "account created"

    except:
        text = "this account is exist"

    context.bot.send_message(
        chat_id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


def custom_create_user(update: Update, context: CallbackContext):

    chat_id = update.message.from_user.id
    context.bot.send_message(
        chat_id,
        text="on development",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r"(Sign up)"), signing_up)],
    states={
        BASE: [
            MessageHandler(
                Filters.regex(r"(with Telegram account)"), default_create_user
            ),
            MessageHandler(Filters.regex(r"(custom sign up)"),
                           custom_create_user),
        ],
    },
    fallbacks=[
        MessageHandler(Filters.text("Cancel"), cancel),
        MessageHandler(Filters.text, wrong_message),
        MessageHandler(Filters.all, error),
    ],
)
