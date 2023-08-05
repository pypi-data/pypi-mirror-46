""" manage users. """

import bot
import logging
import obj
import obj.store

class EUSER(Exception):
    pass

class User(obj.Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(obj.store.Store):

    cache = obj.Object()
    userhosts = obj.Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                logging.warn("allow %s %s" % (origin, ",".join(user.perms)))
                return True
        logging.error("denied %s %s" % (origin, perm))
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                user.save()
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"_type": "bot.users.User", "user": origin}
        return self.all(s)

    def get_user(self, origin, type=None):
        if origin in dir(Users.cache):
            return getattr(Users.cache, origin, None)
        s = {"_type": "bot.users.User", "user": origin}
        res = self.find(s)
        if res:
            u = res[-1]
            Users.cache._set(origin, u)
            return u

    def meet(self, origin, perms=[]):
        user = self.get_user(origin)
        if not user:
            user = User()
        user.user = origin
        user.perms = perms + ["USER", ]
        if perms:
            user.perms.extend(perms)
        user.save(timed=True)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if not user:
            user = User()
            user.user = origin
            user.perms = ["OPER", "USER"]
            user.save()
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise EUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            user.save()
        return user
