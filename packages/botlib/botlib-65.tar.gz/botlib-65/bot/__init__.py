""" bot package. """

__version__ = 65

import bot
import obj

class Cfg(obj.Cfg):

    pass

class Bot(obj.handler.Handler):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.cfg = Cfg()
        self.cfg.update(kwargs)
        self.channels = []
        self.state = obj.Object()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
             self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        from .event import Event
        self.start()
        e = bot.event.Event()
        e.txt = txt
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        from bot.run import kernel
        return kernel.put(event)

    def fileno(self):
        import sys
        return sys.stdin

    def join(self):
        pass

    def raw(self, txt):
        print(txt)

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        if self.verbose:
            self.raw(txt)

    def show_prompt(self):
        pass

    def start(self):
        from .run import kernel
        super().start()
        kernel.add(self)

class OutputCache(obj.Object):

    def add(self, dest, txt):
        if not dest or not txt:
            return
        if "dest" not in self:
            self[dest] = []
        self[dest].append(txt)

    def more(self, dest, nr=10):
        if "dest" in dir(self):
            res = self[dest][-nr:]
            del self[dest][-nr:]
            return res
        return []

class Shell(obj.shell.Shell):

     def dispatch(self, event):
         from .run import kernel
         kernel.put(event)
         event.wait()
         self.show_prompt()

import bot.fleet
import bot.rss