#encoding=utf-8
import asyncio
import aiohttp
from aiohttp import web
import plugins
from burdbot import User

@asyncio.coroutine
def send_msg(msg):
    print(msg)

@asyncio.coroutine
def init(loop):
    print("Testing mode! Type to simulate group chat messages.")
    while True:
        line = input("> ")
        for plugin in plugins.plugins:
            yield from plugin.handle_event(line, User(0, "$User", "$Lastname", "@username") , is_group=True, callback=send_msg)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
