""" list of bots. """

import obj

class Fleet(obj.Object):

    def __init__(self):
        super().__init__()
        self.bots = []

    def __iter__(self):
        return iter(self.bots)

    def add(self, bot):
        self.bots.append(bot)
        return self

    def announce(self, txt):
        for bot in self.bots:
            if bot is self:
                continue
            bot.announce(str(txt))

    def by_type(self, btype):
        res = None
        for bot in self.bots:
            if str(btype).lower() in str(type(bot)).lower():
                res = bot
        return res

    def get_bot(self, bid):
        res = None
        for bot in self.bots:
            if str(bid) in repr(bot):
                res = bot
                break
        return res

    def get_firstbot(self):
        return self.bots[0]

    def match(self, m):
        res = None
        for bot in self.bots:
            if m.lower() in repr(bot):
                res = bot
                break
        return res

    def remove(self, bot):
        self.bots.remove(bot)

    def save(self):
        for bot in self.bots:
            bot.save()

    def say(self, botid, channel, txt):
        bot = self.get_bot(botid)
        if bot:
            bot.say(botid, channel, txt)

    def stop(self):
        for bot in self.bots:
            if bot is self:
                continue
            bot.stop()

    def wait(self):
        for bot in self.bots:
            bot.wait()
