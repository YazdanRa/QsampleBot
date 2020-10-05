from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def say_hello(update: Update, context: CallbackContext):
    context.user_data.clear()
    chat_id = update.message.from_user.id

    context.bot.send_message(
        chat_id,
        "Hello *{}*!".format(update.message.from_user.first_name),
        parse_mode="Markdown",
    )


HANDLER = CommandHandler("start", say_hello)
