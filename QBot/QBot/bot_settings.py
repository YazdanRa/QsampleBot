import os

DJANGO_TELEGRAMBOT = {
    "DISABLE_SETUP": os.getenv("TELEGRAM_DISABLE_SETUP", False),
    "MODE": os.getenv("TELEGRAM_MODE", "POLLING"),
    "STRICT_INIT": True,
    "BOTS": [
        {
            "ID": "Qbot",
            "TOKEN": os.getenv(
                "BOT_TOKEN", "1062412615:AAHLZ974OBY3goSSoX6HePTapjgdJMYFnEY"
            ),
            "CONTEXT": True,
        },
    ],
}
