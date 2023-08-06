""" bot package. """

__version__ = 66

import logging

import bot
import obj

class Cfg(obj.Cfg):

    pass

class Bot(obj.shell.Console):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.cfg = obj.Cfg()
        self.cfg.update(kwargs)
        self.channels = []
        self.state = obj.Object()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
             self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        self.start()
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        return bot.run.kernel.put(event)

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
        super().start()
        bot.run.kernel.add(self)

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

class Event(obj.event.Event):

    def show(self):
        for txt in self._result:
            bot.run.kernel.say(self.orig, self.channel, txt)

class Shell(Bot):

    def dispatch(self, event):
        bot.run.kernel.put(event)
        if not event._func:
            self.raw("\n")
        self.prompt()
        return event

    def get_event(self):
        e = Event()
        e.txt = input()
        e.orig = repr(self)
        e.origin = "root@shell"
        return e

def start(name="botlib", modules=[], version=bot.__version__, wd=obj.hd(".botlib"), shell=False):
    obj.shell.termsave()
    try:
        cfg = obj.shell.parse_cli(name, version=version, wd=wd)
        cfg.shell = shell or cfg.shell
        cfg.modules = ",".join(modules) + "," + cfg.modules
        bot.run.kernel.start()
        bot.run.kernel.initialize(cfg.modules.split(","))
        obj.shell.tail(cfg)
    except KeyboardInterrupt:
        print("")
    except Exception as ex:
        logging.error(obj.get_exception())
    obj.shell.reset()

import bot.cmds
import bot.email
import bot.entry
import bot.event
import bot.fleet
import bot.irc
import bot.kernel
import bot.rss
import bot.run
import bot.udp
import bot.users
