import re
from .plugins import BurdbotPlugin
from asyncio import coroutine

commands_re = re.compile(r"^(/..*?)( +(\w+))?\b")

burdcommands = BurdbotPlugin("Burd commands", author="Athalean", description="A few silly roleplaying commands")

# all attributes of "User" work here, mainly firstname and lastname
# as well as "argument" which is either the firstname of the user
# or the argument they supplied.
commands = {
        "/preen": "*preens {argument} thoroughly*",
        "/cookie": "*tosses a cookie to {argument}*",
        "/coffee": "*opens {argument}'s beak for a hot cup of coffee!*",
        "/tea": "*opens {argument}'s beak for a hot cup of tea!*",
        "/pun": "*plays a rimshot for {argument}'s horrible pun and shakes the pun jar*",
        "/breakfast": "*feeds {argument} a sandwich, a cookie and a choice of tea or coffee*",
        "/fish": "*tosses a fish to {argument}*",
        "/hug": "*hugs {argument} tight* ^v^",
        "/peck": "*pecks at {argument} for attention*",
        "/floof": "*floofs up {argument}*",
        "/energydrink": "*opens {argument}'s beak for an ice cold energy drink*",
}

@burdcommands.trigger
@coroutine
def trigger(text):
    text = text.lower()
    for command in commands.keys():
        if text.startswith(command):
            return True

@burdcommands.helplines
@coroutine
def helptext():
    return [
        '"%s" or "%s <name>"' % (command, command)
        for command in commands.keys()
    ] 

@burdcommands.group_chat
@coroutine
def group(text, sender, response):
    match = commands_re.match(text)
    command, argument = match.group(1), match.group(3)

    context = sender._asdict()
    if argument:
        context["argument"] = argument
    context.setdefault("argument", sender.firstname)

    if command.lower() in commands:
        reaction = commands[command.lower()]
        if isinstance(command, str):
            yield from response(reaction.format(**context))
            return
        yield from reponse((yield from reaction(text, sender)))
