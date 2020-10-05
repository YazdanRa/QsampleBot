import logging

from django_telegrambot.apps import DjangoTelegramBot

from QBot.telegram_bot.views import (
    start,
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Loading handlers for telegram bot")
    bot = DjangoTelegramBot.dispatcher

    handlers = [
        (start.HANDLER, 1),
    ]

    for handler in handlers:
        bot.add_handler(*handler)
