from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

reply_keyboard = [["Sign up", "Login"], ["Home"]]


def say_hello(update: Update, context: CallbackContext):
    context.user_data.clear()
    chat_id = update.message.from_user.id

    context.bot.send_message(
        chat_id,
        "Hello *{}*!".format(update.message.from_user.first_name),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown",
    )


HANDLER = CommandHandler("start", say_hello)
