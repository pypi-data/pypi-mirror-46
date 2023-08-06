""" place to stash runtime objects. """

import sys

from obj.shell import Shell
from obj.tasks import Tasks
from bot.kernel import Kernel
from bot.users import Users

kernel = Kernel()
users = Users()

def cmd(txt):
    s = Shell()
    s.verbose = False
    e = s.cmd(txt)
    e.wait()
    return e

