import re
from .plugins import BurdbotPlugin
from asyncio import coroutine

commands_re = re.compile(r"^(/..*?)\b")

burdcommands = BurdbotPlugin("Burd commands", author="Athalean", description="A few silly commands")

# all attributes of "User" work here, mainly firstname and lastname
commands = {
        "/preen": "*preens {firstname} thoroughly*",
        "/cookie": "*tosses a cookie to {firstname}*",
        "/coffee": "*opens {firstname}'s beak for a hot cup of coffee!*",
        "/tea": "opens {firstname}'s beak for a hot cup of tea!*"
}

@burdcommands.trigger
@coroutine
def trigger(text):
    for command in commands.keys():
        if text.startswith(command):
            return True

@burdcommands.group_chat
@coroutine
def group(text, sender, response):
    command = commands_re.match(text).group(1)
    if command in commands:
        reaction = commands[command]
        if isinstance(command, str):
            yield from response(reaction.format(**sender._asdict()))
            return
        yield from reponse((yield from reaction(text, sender)))
