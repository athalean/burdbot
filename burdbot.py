#encoding=utf-8
import asyncio
import aiohttp
from aiohttp import web
from collections import namedtuple
from functools import partial
import plugins
import json

try:
    from config import *
except ImportError:
    raise ImportError("Can't load settings file config.py. Please create one, following the example of config_sample.py.")

User = namedtuple("User", ["id", "firstname", "lastname", "username"])

@asyncio.coroutine
def send_msg(to, msg):
    if not isinstance(msg, bytearray):
        msg = msg.encode('utf-8')
    yield from aiohttp.request('get', "https://api.telegram.org/bot%s/sendMessage" % API_KEY, params={'chat_id': to, 'text': msg})

@asyncio.coroutine
def handle(request):
    data = json.loads((yield from request.content.read()).decode('utf-8'))
    if 'message' not in data:
        return web.Response(body="ok".encode('utf-8'))
    data = data['message']
    from_info = data.get('from', {})

    if not from_info:
        sender = None
    else:
        sender_id = from_info.get('id', 0)
        sender_first = from_info.get('first_name', "Anonymous someone")
        sender_last = from_info.get('last_name', "whose name is unknown")
        sender_username = from_info.get('username', 'anonymous')
        sender = User(sender_id, sender_first, sender_last, sender_username)

    is_group_chat = 'title' in data.get('chat', {})
    reply_id = data.get('chat').get('id')
    message = data.get('text', '').strip()

    for plugin in plugins.plugins:
        try:
            yield from plugin.handle_event(message, sender, is_group_chat, partial(send_msg, reply_id))
        except:
            continue 

    return web.Response(body="ok".encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('POST', '/', handle)
    srv = yield from loop.create_server(app.make_handler(),
            ADDRESS, PORT)
    print("Server started at http://%s:%d" % (ADDRESS, PORT))
    return srv

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
