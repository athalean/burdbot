from asyncio import coroutine

class BurdbotPlugin:
    def __init__(self, name, author=None, description=None):
        self.name = name
        self.author = author
        self.description = None
        
        self.trigger_func = None
        self.groupchat_func = None
        self.helptext_func = None

    def trigger(self, f):
        """Sets a callback coroutine that every incoming line is checked against. If
        it doesn't return a true-ish value, the line will be ignored by the
        plugin. It should avoid doing any complicated parsing as it is executed for every
        line received."""
        self.trigger_func = f

    def helplines(self, f):
        """Sets a callback coroutine that return a list of strings. This is used
        to construct the /help command output"""
        self.helptext_func = f

    def group_chat(self, f):
        """Sets a callback coroutine that is being called on an incoming group chat message
        that has passed the trigger. (see trigger)"""
        self.groupchat_func = f

    @coroutine
    def handle_event(self, message, sender, is_group, callback):
        """Handle an incoming Telegram event. Can be a group or a private message."""
        if not self.trigger_func or not (yield from self.trigger_func(message)):
            return

        if is_group and self.groupchat_func:
            return (yield from self.groupchat_func(message, sender, callback))

