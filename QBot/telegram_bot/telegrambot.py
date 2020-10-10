import logging

from django_telegrambot.apps import DjangoTelegramBot

from .views import (
    start,
    sign_up,
    login,
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Loading handlers for telegram bot")
    bot = DjangoTelegramBot.dispatcher

    handlers = [
        (start.HANDLER, 1),
        (sign_up.HANDLER, 1),
        (login.HANDLER, 1),
    ]

    for handler in handlers:
        bot.add_handler(*handler)
