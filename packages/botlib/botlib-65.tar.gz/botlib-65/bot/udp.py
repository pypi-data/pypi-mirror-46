""" udp to channel relay. """

import logging
import socket
import time

from bot.run import kernel
from obj.base import Dotted
from obj.tasks import launch

def init():
    server = UDP()
    server.start()
    return server

class Cfg(Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.host = "localhost"
        self.port = 5500
        self.password = "boh"
        self.seed = "blablablablablaz" # needs to be 16 chars wide
        self.server = self.host
        self.owner = ""

class UDP(Dotted):

    def __init__(self):
        super().__init__(self)
        self._stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def exit(self):
        self._stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("bla", "utf-8"), (self.cfg.host, self.cfg.port))

    def join(self):
        pass

    def server(self, host="", port=""):
        c = self.cfg
        self._sock.bind((host or c.host, port or c.port))
        logging.warning("listening at %s:%s" % (host or c.host, port or c.port))
        while not self._stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self._stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)
        txt = "stop %s:%s" % (c.host, c.port)
        logging.info(txt)

    def start(self):
        s = {"_type": "bot.udp.Cfg"}
        last = kernel.last(s)
        if last:
            self.cfg.update(last)
        launch(self.server)

    def output(self, txt, addr=None):
        try:
            (passwd, text) = txt.split(" ", 1)
        except ValueError:
            return
        text = text.replace("\00", "")
        if passwd == self.cfg.password:
            for bot in kernel.bots:
                bot.announce(text)
