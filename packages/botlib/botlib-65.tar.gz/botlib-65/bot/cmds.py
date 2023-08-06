""" basic bot commands. """

import obj

from .run import kernel, users

def dump(event):
    event.reply(kernel)

def fleet(event):
    try:
        nr = int(event.args[0])
    except (IndexError, ValueError):
        event.reply(str([obj.get_type(b) for b in kernel.bots]))
        return
    try:
        event.reply(str(kernel.bots[nr]))
    except IndexError:
        pass

def load(event):
    if not event.args:
        event.reply("|".join(sorted(obj.loader.table.keys())))
        return
    name = event.args[0]
    try:
        mod = kernel.walk(name, True)
    except ModuleNotFoundError:
        event.reply("module %s not found." % name)
        return
    except:
        event.reply(obj.get_exception())
    event.reply("%s loaded" % name)

def meet(event):
    from .run import users
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("|".join(sorted(users.userhosts.keys())))
        return
    origin = getattr(users.userhosts, origin, origin)
    u = users.meet(origin, perms)
    event.reply("added %s" % u.user)

def unload(event):
    if not event.args:
        event.reply("|".join(sorted(obj.loader.table.keys())))
        return
    name = event.args[0]
    try:
        del obj.loader.table[name]
    except KeyError:
        event.reply("%s is not loaded." % name)        
        return
    event.reply("unload %s" % name)
