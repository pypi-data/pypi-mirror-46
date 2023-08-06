""" bot package. """

__version__ = 68

import logging
import sys

import bot
import obj

class Cfg(obj.Cfg):

    pass

class Bot(obj.handler.Handler):

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

class Console(obj.shell.Shell):

    def announce(self, txt):
        pass

    def dispatch(self, event):
        event.parse(event.txt)
        bot.run.kernel.put(event)
        event.wait()
        if not event._func and self.verbose:
            self.raw("\n")
        if self.verbose:
            self.prompt()
        return event

    def get_event(self):
        e = Event()
        e.txt = input()
        e.orig = repr(self)
        e.origin = "root@shell"
        return e

    def prompt(self):
        if self.verbose:
            self.raw("> ")
            sys.stdout.flush()

def start(name="botlib", modules=[], version=bot.__version__, wd=obj.hd(".botlib"), shell=False):
    obj.shell.termsave()
    try:
        cfg = obj.shell.parse_cli(name, version=version, wd=wd)
        cfg.shell = cfg.shell or shell
        if cfg.modules:
            cfg.modules = ",".join(modules) + "," + cfg.modules
        bot.run.kernel.start()
        tail(cfg)
    except KeyboardInterrupt:
        print("")
    except Exception as ex:
        logging.error(obj.get_exception())
    obj.shell.reset()

def tail(cfg):
    if cfg.args:
        e = obj.cmd(" ".join(cfg.args))
        for txt in e._result:
            print(txt)
        return e
    elif cfg.shell:
        c = Console()
        bot.run.kernel.add(c)
        c.verbose = True
        c.start()
        c.prompt()
        c.wait()

import bot.cmds
import bot.entry
import bot.event
import bot.fleet
import bot.irc
import bot.kernel
import bot.run
import bot.users
