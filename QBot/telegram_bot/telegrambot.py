import logging

from django_telegrambot.apps import DjangoTelegramBot

from . import services, GlobalHandler
from .views import (
    start,
    register,
    login,
)

logger = logging.getLogger(__name__)


def process_update(update, context):
    services.process_update(update, "Qbot")


UPDATE_PROCESS_HANDLER = GlobalHandler(process_update)


def main():
    logger.info("Loading handlers for telegram bot")
    bot = DjangoTelegramBot.dispatcher

    handlers = [
        (UPDATE_PROCESS_HANDLER, 0),
        (start.HANDLER, 1),
        (register.HANDLER, 2),
        (login.HANDLER, 3),
    ]

    for handler in handlers:
        bot.add_handler(*handler)

    bot.add_error_handler(services.process_error)
