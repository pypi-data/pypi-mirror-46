""" IRC bot module. """

import _thread
import bot
import logging
import obj
import os
import queue
import re
import socket
import ssl
import textwrap
import time
import threading

from obj.shell import parse_cli

from .event import Event
from .run import kernel, users

def init():
    bot = IRC()
    bot.walk("bot.cmds")
    bot.start()
    return bot

class Cfg(obj.Cfg):

    def __init__(self):
        super().__init__()
        self.blocking = 1
        self.channel = ""
        self.ipv6 = False
        self.nick = ""
        self.port = 6667
        self.realname = "botlib"
        self.resume = ""
        self.server = ""
        self.ssl = False
        self.username = "bot"
        self.verbose = False

class IEvent(bot.event.Event):

    def __init__(self):
        super().__init__()
        self.arguments = []
        self.cc = ""
        self.channel = ""
        self.command = ""
        self.nick = ""
        self.target = ""

class DEvent(bot.event.Event):

    def __init__(self):
        super().__init__()
        self._sock = None
        self._fsock = None
        self.channel = ""

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 500

class IRC(bot.Bot):

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._threaded = True
        self.cc = "!"
        self.cfg = Cfg()
        self.channels = []
        self.state = obj.Object()
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.state.resume = None
        self.register("352", self.handler)
        self.register("366", self.handler)
        self.register("376", self.handle_connect)
        self.register("433", self.handler)
        self.register("ERROR", self.handle_error)
        self.register("MODE", self.handler)
        self.register("PING", self.handler)
        self.register("PONG", self.handler)
        self.register("PRIVMSG", self.handle_privmsg)

    def _parsing(self, txt):
        rawstr = str(txt)
        o = IEvent()
        o.txt = rawstr
        o.cc = self.cc
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        o.origin = arguments[0]
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                    o.txt = " ".join(txtlist)
        else:
            o.cmd = o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        if o.arguments:
            o.target = o.arguments[-1]
        else:
            o.target = ""
        if o.target.startswith("#"):
            o.channel = o.target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        o.args = o.txt.split()
        o.orig = repr(self)
        o.rest = " ".join(o.args)
        return o

    def _some(self, use_ssl=False, encoding="utf-8"):
        if use_ssl:
            inbytes = self._sock.read()
        else:
            inbytes = self._sock.recv(512)
        txt = str(inbytes, encoding)
        if txt == "":
            raise ConnectionResetError
        txt = bytes(txt, "utf-8").decode("unicode_escape")
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
            if not s.startswith("PING") and not s.startswith("PONG"):
                logging.warning(s.strip())
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self.say(repr(self), channel, txt)

    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self):
        oldsock = None
        if self.cfg.resume:
            s = {"_type": "bot.irc.IRC"}
            bot = kernel.last(s)
            if bot:
                fd = int(bot.state["resume"])
                self.state.resume = fd
                logging.warn("resume %s" % fd)
            else:
                fd = self._sock.fileno()
            if self.cfg.ipv6:
                oldsock = socket.fromfd(fd , socket.AF_INET6, socket.SOCK_STREAM)
            else:
                oldsock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        if not oldsock:
            if self.cfg.ipv6:
                oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:
                oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(int(self.cfg.blocking or 1))
        oldsock.settimeout(60.0)
        if not self.cfg.resume:
            oldsock.connect((self.cfg.server, int(self.cfg.port or 6667)))
        oldsock.setblocking(int(self.cfg.blocking))
        oldsock.settimeout(700.0)
        if self.cfg.ssl:
            self._sock = ssl.wrap_socket(oldsock)
        else:
            self._sock = oldsock
        self.state.resume = self._sock.fileno()
        self._fsock = self._sock.makefile("r")
        os.set_inheritable(self.state.resume, os.O_RDWR)
        self._connected.set()
        logging.warning("connect %s %s" % (self.cfg.server, self.cfg.port or 6667))
        return True

    def dispatch(self, event):
        if event.command:
            func = self.get_handler(event.command)
            if func:
                func(event)
            return
        super().dispatch(event)

    def get_event(self):
        if not self._buffer:
            try:
                self._some()
            except socket.timeout as ex:
                e = IEvent()
                e._error = obj.get_exception()
                e.command = "ERROR"
                return e
        return self._parsing(self._buffer.pop(0))

    def handle_connect(self, event):
        if "servermodes" in dir(self.cfg):
            self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
        self.joinall()

    def handle_error(self, event):
        logging.error(event.txt)
        self.state.error = event

    def handle_privmsg(self, event):
        users.userhosts.set(event.nick, event.origin)
        if not users.allowed(event.origin, "USER"):
            return
        if event.txt.startswith("\001DCC"):
            try:
                dcc = DCC()
                kernel.add(dcc)
                dcc.encoding = "utf-8"
                obj.launch(dcc.connect, event)
                return
            except ConnectionRefusedError:
                return
        elif event.txt.startswith("\001VERSION"):
            txt = "\001VERSION %s %s - %s\001" % ("BOTLIB", bot.__version__, bot.__txt__)
            self.command("NOTICE", event.channel, txt)
            return
        if event.txt and event.txt[0] == self.cc:
            event.txt = event.txt[1:]
        kernel.put(event)

    def handler(self, event):
        cmd = event.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", event.txt)
        elif cmd == "PONG":
            self.state.pongcheck = False
        elif cmd == "433":
            nick = event.target + "_"
            self.cfg.nick = nick
            self.command("NICK", nick)

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        self._connected.wait()
        self.raw("NICK %s" % nick, True)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname), True)

    def loop(self):
        try:
            self._connected.wait()
            super().loop()
        except ConnectionResetError:
            self.stop()
            self.start()

    def output(self):
        self._connected.wait()
        while not self._stopped:
            channel, txt = self._outqueue.get()
            if not channel and not txt:
                break
            self.command("PRIVMSG", channel, txt)

    @obj.locked
    def raw(self, txt, direct=False):
        self._connected.wait()
        txt = txt.rstrip()
        if self._stopped:
            return
        if not txt.startswith("PING") and not txt.startswith("PONG"):
            logging.warning(txt)
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        if not direct:
            if (time.time() - self.state.last) < 3.0:
                time.sleep(1.0 * (self.state.nrsend % 10))
        self.state.last = time.time()
        self.state.nrsend += 1
        self._sock.send(txt)

    def resume(self):
        super().start()
        obj.launch(self.output)
        self.announce("done")

    def say(self, orig, channel, txt):
        wrapper = TextWrap()
        txt = str(txt)
        for line in txt.split("\n"):
            for t in wrapper.wrap(line):
                self._outqueue.put((channel, t))

    def start(self):
        #p, last = obj.store.last("bot.irc.Cfg")
        #if last:
        #    self.cfg.update(last)
        self.cfg.update(obj.cfg, skip=True)
        self.cfg.update(obj.cfg)
        #self.cfg.save(p)
        if not self.cfg.channel and obj.cfg.shell:
            logging.error("missing channel, use -c option")
            return
        if not self.cfg.server and obj.cfg.shell:
            logging.error("missing server, use -s option")
            return
        if self.cfg.channel:
            self.channels.append(self.cfg.channel)
        nr = 1
        self.state.error = ""
        super().start()
        obj.launch(self.output)
        while 1:
            try:
                self.connect()
                break
            except socket.gaierror as ex:
                logging.warn(ex)
                break
            except ConnectionRefusedError:
                txt = "%s connection refused" % self.cfg.server
                logging.warning(txt)
                break
            time.sleep(nr * 3.0)
            nr += 1
        if not self.cfg.resume and not self.state.error:
            self.logon(self.cfg.server, self.cfg.nick)
        return self

    def stop(self):
        self._stopped = True
        super().stop()
        self._outqueue.put_nowait((None, None))
        self.ready()

class DCC(bot.Bot):

    def __init__(self):
        super().__init__()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def announce(self, txt):
        self.raw(txt)

    def connect(self, event):
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4][:-1]
        port = int(port)
        if re.search(':', addr):
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.send(bytes('Welcome to %s %s !!\n' % (obj.cfg.name, event.nick), "utf-8"))
        s.setblocking(True)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.origin = event.origin
        super().start()

    def errored(self, event):
        self.state.error = event
        logging.error(str(event))

    def event(self, txt):
        e = DEvent()
        e.txt = txt
        e._sock = self._sock
        e._fsock = self._fsock
        e.orig = repr(self)
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        return e

    def get_event(self):
        txt = self._fsock.readline()
        return self.event(txt)

    def raw(self, txt):
        self._fsock.write(txt.rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def say(self, orig, channel, txt):
        self.raw(txt)
