# Burdbot

Burdbot is a silly but sometimes helpful Telegram bot.

## Dependencies

* **Python 3.4+**
* aiohttp


## Plugin boilerplate

    from asyncio import coroutine
    from .plugins import BurdbotPlugin

    myplugin = BurdbotPlugin("My Plugin", author="Me")

    @myplugin.trigger
    @coroutine
    def trigger(text):
        """Return True here to indicate that your plugin could want to react to this line"""

    @myplugin.group_chat
    @coroutine
    def reaction(text, sender, respond):
        """Program your actual reaction in this coroutine"""
        yield from respond("Hello, %s!", sender.firstname)
