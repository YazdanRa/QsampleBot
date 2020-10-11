import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    Filters,
    MessageHandler,
    CommandHandler,
)

from .error import wrong_message, cancel
from user.models import CustomUser
from telegram_bot.models import TelegramUser

# logger
logger = logging.getLogger(__name__)

# states
USERNAME, PASSWORD, PHONE_NUMBER = range(3)

# keyboard
KEYBOARD = [
    ["Folan", "bisar"],
    ["button 1", "button 2", "button 3"],
    ["Logout"],
    ["contact us", "support"],
]


def start_register(update: Update, context: CallbackContext):
    context.user_data.clear()
    chat_id = update.message.from_user.id

    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "Enter your username\n"
            "the username only can contain english letters and numbers and (_).\n"
            "you can use your telegram username for that :)"
        ),
        reply_markup=ReplyKeyboardMarkup(
            [[update.message.from_user.username]],
            one_time_keyboard=True,
        ),
    )
    return USERNAME


def get_username(update, context):
    chat_id = update.message.from_user.id
    username = update.message.text

    # validate username
    if not CustomUser.objects.get(username__iexact=username).exists():
        context.bot.send_message(
            chat_id=chat_id,
            text="this username already taken by another user, please enter another one:",
        )
        return  # it means this user will keep in this state again!

    context.user_data["username"] = username
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "now enter your password\n"
            "The password should match by the following regex:\n"
            "`^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`"
        ),
        parse_mode="Markdown",
    )
    return PASSWORD


def get_password(update, context):
    chat_id = update.message.from_user.id
    password = update.message.text
    context.user_data["password"] = password

    # remove the password from messages for security issues
    context.bot.delete_message(chat_id, update.message.message_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "now enter your phone_number\n"
            "phone_number should start with 09 and match in the following regex:\n"
            "`^(09)\d{9}$`"
        ),
    )
    return PHONE_NUMBER


def get_phone_number(update, context):
    chat_id = update.message.from_user.id
    phone_number = update.message.text

    # create user
    try:
        telegram_user = TelegramUser.objects.get(chat_id=chat_id)
        user = CustomUser.objects.create(
            username=context.user_data.get("username"),
            password=context.user_data.get("password"),
            phone_number=phone_number,
            telegram=telegram_user,
        )
    except TelegramUser.DoesNotExist as err:
        logger.exception(err)
        # TODO: send a signal for developers!
        #       to find out more search about "django signals"
        pass

    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "you are successfully registered and logged in!\n"
            "*Welcome to Qbot*\n"
            "you can use commands and keyboard to use the bot\n"
            "Enjoy it :)"
        ),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            KEYBOARD,
            one_time_keyboard=True,
        ),
    )

    return ConversationHandler.END


HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.text("register"), start_register)],
    states={
        USERNAME: [MessageHandler(Filters.regex(pattern=r"\w+"), get_username)],
        PASSWORD: [
            MessageHandler(
                Filters.regex(
                    pattern=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
                ),
                get_password,
            )
        ],
        PHONE_NUMBER: [
            MessageHandler(Filters.regex(pattern=r"^(09)\d{9}$"), get_phone_number)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(Filters.text, wrong_message),
    ],
)
