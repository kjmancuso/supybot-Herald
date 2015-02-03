###
# Copyright (c) 2014, Kevin Mancuso
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.httpserver as httpserver

import supybot.ircmsgs as ircmsgs

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Herald')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


# HTTP Server? Lol
class HeraldServerCallback(httpserver.SupyHTTPServerCallback):
    name = 'Herald'
    defaultResponse = """
    Something will need to be added here."""

    def doPost(self, handler, path, form):
        if not form.getvalue('chan'):
            self.error('Error: No channel provided')
            return
        if not form.getvalue('msg'):
            self.error('Error: No message provided')
            return
        chan = form.getvalue('chan')
        msg = form.getvalue('msg')
        msg = ircutils.bold('[Announce] ') + msg
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.plugin.say(chan, msg)
        self.wfile.write('OK')

    def error(self, reason):
        self.send_response(500)
        self.wfile.write(reason)


class Herald(callbacks.Plugin):
    """Add the help for "@plugin help Herald" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Herald, self)
        callbacks.Plugin.__init__(self, irc)
        self.irc = irc

        callback = HeraldServerCallback()
        # Insert callbacks.Plugin into the ole httpservercallback class
        callback.plugin = self
        httpserver.hook('herald', callback)

    def die(self):
        httpserver.unhook('herald')

        self.__parent.die()

    def say(self, chan, msg):
        self.irc.queueMsg(ircmsgs.privmsg(chan, msg))


Class = Herald


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
