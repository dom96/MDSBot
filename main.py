#!/usr/bin/env python
'''
Created on 2009-12-16

@author: Dominik
'''
import XmlHelper
usrManager = XmlHelper.load_users()
factoidManager = XmlHelper.load_factoids()
loadedSettings = XmlHelper.loadSettings()
print loadedSettings['nicks']

import relay
relayManager = relay.relay_manager()

from IRCLibrary import IRC
addresses = loadedSettings['addresses']
s = IRC.connection(addresses, loadedSettings['nicks'], \
        loadedSettings['realname'], loadedSettings['username'])
s.autojoinchans = loadedSettings['channels']

loadedModules = {}
for module in loadedSettings['modules']:
    import imp, os, sys
    try:
        loadedModules[module] = imp.load_source(module, \
            os.path.join(os.path.dirname(sys.argv[0]), "modules/%s/%s.py" % (module, module)))
        loadedModules[module].main(s, "", usrManager)
    except IOError:
        import traceback; traceback.print_exc()
        print "Error: module '%s' could not be found." % (module)

def main():

    print "MDSBot 0.1 initialized"
    print "Using version " + IRC.version + " IRCLibrary"

    import sys
    sys.path.append("modules")

    s.events.hook_event("QUIT", quit_logout)
    
    s.events.hook_event("PRIVMSG", privmsg)
    s.events.hook_event("disconnect", disconnect)
    s.connect(pingServ=False, threaded=False)

    # TODO: having .connect not calling .response would make more sense...

def disconnect(server, word, word_eol, args):
    import sys; sys.exit(1)
    
def privmsg(server, word, word_eol, args):
    import commands
    try:
        commands.cmd(server, word, word_eol, usrManager, relayManager, factoidManager, loadedModules)
    except:
        import traceback; traceback.print_exc()
    
def quit_logout(server, word, word_eol, args):
    usrManager.change_user_status(word[0].split("!")[0], False)
    
if __name__ == '__main__':
    main()
        
        
        
