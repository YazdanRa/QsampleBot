from django.utils.timezone import now
from telegram import Update
from telegram.ext import CallbackContext

from .models import TelegramUpdate, TelegramUser


def process_error(update: Update, context: CallbackContext):
    try:
        # TODO: log the exception in sentry_sdk and logger
        context.bot.send_message(
            update.message.chat.id,
            "We have encountered an internal error!\n"
            "Our team is notified and is working on this problem.\n"
            "Sorry for the inconvenience.",
        )
    except:
        pass
    raise context.error


def process_update(update: Update, bot: str):
    def get_message_users(message):
        users = [
            message.get("from", None),
            message.get("forward_from", None),
            message.get("left_chat_member", None),
        ]
        for user in message.get("new_chat_members", []):
            users.append(user)

        if message.get("reply_to_message", None):
            users += get_message_users(message["reply_to_message"])

        if message.get("pinned_message", None):
            users += get_message_users(message["pinned_message"])

        return users

    users = []
    if update.message:
        users += get_message_users(update.message.to_dict())

    if update.edited_message:
        users += get_message_users(update.edited_message.to_dict())

    users = [
        user for user in users if user is not None and user.get("id", None) is not None
    ]  # Remove None values
    users = list(
        {user["id"]: user for user in users}.values()
    )  # Remove duplicate users

    for user in users:
        try:
            current_user = TelegramUser.objects.get(id=user["id"])
            TelegramUser.objects.filter(id=user["id"]).update(
                first_name=user["first_name"],
                last_name=user.get("last_name", None),
                is_bot=user["is_bot"],
                username=user.get("username", None),
                language_code=user.get("language_code", None),
                bots=list(set(current_user.bots + [bot])),
                last_seen=now(),
            )
        except TelegramUser.DoesNotExist:
            TelegramUser.objects.update_or_create(
                id=user["id"],
                first_name=user["first_name"],
                last_name=user.get("last_name", None),
                is_bot=user["is_bot"],
                username=user.get("username", None),
                language_code=user.get("language_code", None),
                bots=[bot],
                last_seen=now(),
            )

    TelegramUpdate.objects.create(
        update_id=update.update_id,
        bot=bot,
        message=update.message.to_json() if update.message else None,
        edited_message=update.edited_message.to_json()
        if update.edited_message
        else None,
        channel_post=update.channel_post.to_json() if update.channel_post else None,
        edited_channel_post=update.edited_channel_post.to_json()
        if update.edited_channel_post
        else None,
        inline_query=update.inline_query.to_json() if update.inline_query else None,
        chosen_inline_result=update.chosen_inline_result.to_json()
        if update.chosen_inline_result
        else None,
        callback_query=update.callback_query.to_json()
        if update.callback_query
        else None,
    )
