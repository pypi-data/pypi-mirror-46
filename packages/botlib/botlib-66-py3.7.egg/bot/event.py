""" event handler. """

import logging
import bot
import obj
import threading

class Event(obj.event.Event):

    def __init__(self):
        super().__init__()
        self._trace = ""
        self.batched = True

    def display(self):
        for txt in self._result:
            bot.run.kernel.announce(txt)

    def show(self):
        b = bot.run.kernel.get_bot(self.orig)
        if not b:
            logging.error("missing register from %s" % self.orig)
            return
        for txt in self._result:
            b.say(self.orig, self.channel, txt)
