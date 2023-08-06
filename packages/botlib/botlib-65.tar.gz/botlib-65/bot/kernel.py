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

from bot import Bot
from bot.fleet import Fleet
from obj import Cfg, Store, cfg
from obj.event import Event
from obj.handler import Handler
from obj.loader import table, handlers
from obj.shell import Console, defaults, parse_cli, reset, termsave

class Cfg(Cfg):

    pass    

class Event(Event):

    def show(self):
        from .run import kernel
        for txt in self._result:
            kernel.say(self.orig, self.channel, txt)

class Shell(Console, Bot):

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
        self.cfg.update(defaults)

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

    def start(self, name="bot", modules=[], version=bot.__version__, wd="", shell=False):
        termsave()
        try:
            wd = obj.hd(".bot")
            cfg = parse_cli(name, version=version, wd=wd)
            cfg.shell = shell or cfg.shell
            obj.cfg.update(cfg)
            self.cfg.update(cfg)
            self.cfg.verbose = self.cfg.shell
            self.cfg.modules = ",".join(modules) + "," + cfg.modules
            self.initialize(self.cfg.modules.split(","))
            super().start()
            obj.shell.tail(cfg)
        except KeyboardInterrupt:
            print("")
        except Exception as ex:
            logging.error(obj.get_exception())
        reset()

    def tail(self):
        if self.cfg.args:
            e = obj.cmd(" ".join(self.cfg.args))
            e.wait()
        elif self.cfg.shell:
            shell = Shell()
            shell.start()
            self.add(shell)
            if not self.cfg.args:
                shell.verbose = True
                shell.prompt()
                shell.wait()
