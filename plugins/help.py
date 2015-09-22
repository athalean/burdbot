from asyncio import coroutine
from .plugins import BurdbotPlugin

help_plugin = BurdbotPlugin("Help Command", author="Athalean", description="A /help command that lists commands and features, as defined by plugins")

@help_plugin.trigger
@coroutine
def trigger(text):
    return text.lower().startswith("/help")

@help_plugin.helplines
@coroutine
def help():
    return ['"/help" - Show this help']

@help_plugin.group_chat
@coroutine
def reaction(text, sender, respond):
    response = "Hi, I'm Burdbot! I'm here to entertain you all and sometimes to do something useful. ^v^\n\nI can do the following commands and features:\n\n"
    from . import plugins
    lines = []
    for plugin in plugins:
        if plugin.helptext_func:
            lines.extend((yield from plugin.helptext_func()))
    yield from respond(response + '\n'.join(' *  '+line for line in sorted(lines, key=lambda line: line.replace("\"", ""))))
