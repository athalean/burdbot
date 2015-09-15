from asyncio import coroutine
from .plugins import BurdbotPlugin
from random import random, choice

randomchirp = BurdbotPlugin("Random chirping", author="Athalean", description="Lets the bot randomly respond.")

@randomchirp.trigger
@coroutine
def trigger(text):
    return random() <= 0.02 # chance: about once every 50 lines

@randomchirp.group_chat
@coroutine
def reaction(text, sender, respond):
    yield from respond(choice(["chirp", "ovo"]))
