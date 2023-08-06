""" boot code initialisation and main loop. """

import logging
import os
import readline
import sys
import threading
import time

import bot
import obj

class Cfg(obj.Cfg):

    pass    

class Kernel(bot.fleet.Fleet, obj.handler.Handler, obj.Store):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.cfg.update(obj.shell.defaults)

    def initialize(self, mods):
        res = []
        thrs = []
        exclude = obj.cfg.exclude.split(",")
        for m in mods:
            if not m or m in exclude:
                continue
            logging.warn("init %s" % m)
            try:
                thrs = self.walk(m, True)
                for thr in thrs:
                    thr.join()
            except Exception as ex:
                logging.error(obj.get_exception())

    def start(self):
        self.cfg.update(obj.cfg)
        self.initialize(self.cfg.modules.split(","))
        super().start()
