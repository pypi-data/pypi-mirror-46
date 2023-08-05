""" boot code initialisation and main loop. """

import bot
import logging
import obj
import obj.loader
import os
import readline
import sys
import threading
import time

from bot.fleet import Fleet
from obj import Cfg, cfg
from obj.command import Command
from obj.handler import Handler
from obj.loader import table, handlers
from obj.shell import Console, boot, defaults, reset, termsave
from obj.store import Store

class Cfg(Cfg):

    pass    

class Event(Command):

    def show(self):
        from .run import kernel
        for txt in self._result:
            kernel.say(self.orig, self.channel, txt)

class Shell(Console):

    def dispatch(self, event):
        from .run import kernel
        kernel.dispatch(event)
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

class Kernel(Fleet, Handler, Store):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.cfg._update(defaults)

    def dispatch(self, event):
        event.parse(event.txt)
        event._func = self.get_cmd(event)
        if event._func:
            logging.warn("dispatch %s" % event.txt)
            event._func(event)
            event.show()
        event.ready()

    def initialize(self, mods):
        res = []
        thrs = []
        for m in mods:
            if not m:
                continue
            try:
                thrs = self.walk(m, True)
                for thr in thrs:
                    thr.join()
            except Exception as ex:
                logging.error(obj.get_exception())

    def run(self, name, modules=[], version=bot.__version__, wd=obj.hd(".botlib"), shell=False):
        termsave()
        try:
            self.cfg = boot(name, version, wd)
            self.cfg.verbose = self.cfg.shell
            self.cfg.modules += "," + ",".join(modules)
            self.start()
            self.tail(shell and self.cfg.shell)
        except KeyboardInterrupt:
            print("")
        except Exception as ex:
            logging.error(obj.get_exception())
        reset()

    def start(self):
        self.walk("bot.cmds")
        self.initialize(self.cfg.modules.split(","))
        super().start()
        return self    

    def tail(self, shell):
        if self.cfg.args:
            e = obj.cmd(" ".join(cfg.args))
            e.wait()
        elif shell:
            shell = Shell()
            shell.start()
            self.add(shell)
            if not self.cfg.args:
                shell.verbose = True
                shell.prompt()
                shell.wait()
