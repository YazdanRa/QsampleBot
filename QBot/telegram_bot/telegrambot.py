import logging

from django_telegrambot.apps import DjangoTelegramBot

from .views import (
    start,
    register,
    login,
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Loading handlers for telegram bot")
    bot = DjangoTelegramBot.dispatcher

    handlers = [
        (start.HANDLER, 1),
        (register.HANDLER, 2),
        (login.HANDLER, 3),
    ]

    for handler in handlers:
        bot.add_handler(*handler)
