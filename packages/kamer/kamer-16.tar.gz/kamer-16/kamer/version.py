# kamer/version.py
#
#

""" version plugin. """

from kamer import __version__

txt = """ straffeloosheid zekerende kamerleden de cel in !! """

def version(event):
    event.reply("KAMER #%s - %s" % (__version__, txt))
