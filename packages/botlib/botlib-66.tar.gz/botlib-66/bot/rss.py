""" feed fetcher. """

import logging
import re
import bot.rss
import obj

from obj.utils import file_time, get_feed, strip_html, to_time, unescape
from .run import kernel

def init():
    fetcher = Fetcher()
    fetcher.start()
    return fetcher

class Cfg(obj.Cfg):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_list = ["title", "link"]
        self.summary = []

class Seen(obj.Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Feed(obj.Object):

    pass

class Fetcher(obj.Object):

    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []
        self.cfg = Cfg()

    def display(self, o):
        result = ""
        if "display_list" in dir(obj):
            dl = o.display_list
        else:
            dl = self.cfg.display_list
        for key in dl:
            if key == "summary":
                skip = False
                for txt in self.cfg.summary:
                    if txt not in o.link:
                        skip = True
                if skip:
                    continue
            data = o.get(key, None)
            if data:
                data = str(data)
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = re.sub(r"\s+", " ", data)
                data = unescape(data)
                result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        counter = 0
        objs = []
        for o in get_feed(rssobj.rss):
            if not o:
                continue
            feed = Feed()
            feed.update(o)
            if feed.link in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(feed.link)
            counter += 1
            objs.append(feed)
            if "updated" in dir(feed):
                date = file_time(to_time(feed.updated))
                feed.save(stime=date)
                continue
            elif "published" in dir(feed):
                date = file_time(to_time(feed.published))
                feed.save(stime=date)
                continue
            feed.save()
        Fetcher.seen.save()
        for obj in objs:
            txt = self.display(obj)
            kernel.announce(txt)
        return counter

    def join(self):
        for thr in self._thrs:
            thr.join()

    def run(self):
        for p, o in kernel.all("bot.rss.Rss"):
            self._thrs.append(obj.launch(self.fetch, o))
        return self._thrs

    def start(self, repeat=True):
        p, last = kernel.last("bot.rss.Cfg")
        if last:
            self.cfg.update(last)
            self.cfg.save()
        prev = obj.Cfg()
        prev.update(self.cfg)
        self.cfg.update(obj.cfg)
        if self.cfg != prev:
            self.cfg.save(p)
        last_seen = obj.last("bot.rss.Seen")
        if last_seen:
            Fetcher.seen.update(last_seen)
        if repeat:
            repeater = obj.clock.Repeater(600, self.run)
            repeater.start()
            return repeater

    def stop(self):
        Fetcher.seen.save()

class Rss(obj.Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

def fetch(event):
    fetcher = Fetcher()
    fetcher.start(repeat=False)
    thrs = fetcher.run()
    res = []
    for thr in thrs:
        res.append(thr.join())
    event.reply("fetched %s" % ",".join([str(x or "0") for x in res]))

def rss(event):
    if not event.rest or "http" not in event.rest:
        event.reply("rss <url>")
        return
    o = Rss()
    o.rss = event.rest
    o.save()
    event.reply("ok 1")

obj.types.append("bot.rss.Rss")
obj.classes["rss"] = "bot.rss.Rss"
obj.classes["feed"] = "bot.rss.Feed"
obj.args["rss"] = ["rss",]
