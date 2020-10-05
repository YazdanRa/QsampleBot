# Django Telegram Bot settings
import os

DJANGO_TELEGRAMBOT = {
    'MODE': 'POLLING',
    'BOTS': [
        {
            'TOKEN': os.getenv("BOT_TOKEN"),  # Your bot token.
            'CONTEXT': True,
            # 'POLL_INTERVAL' : (Optional[float]), # Time to wait between polling updates from Telegram in
            # seconds. Default is 0.0

            # 'POLL_CLEAN':(Optional[bool]), # Whether to clean any pending updates on Telegram servers before
            # actually starting to poll. Default is False.

            # 'POLL_BOOTSTRAP_RETRIES':(Optional[int]), # Whether the bootstrapping phase of the `Updater`
            # will retry on failures on the Telegram server.
            # |   < 0 - retry indefinitely
            # |     0 - no retries (default)
            # |   > 0 - retry up to X times

            # 'POLL_READ_LATENCY':(Optional[float|int]), # Grace time in seconds for receiving the reply from
            # server. Will be added to the `timeout` value and used as the read timeout from
            # server (Default: 2).
        },
        # Other bots here with same structure.
    ],

}
