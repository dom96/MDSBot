#!/usr/bin/env python
'''
Created on 2009-12-16

@author: Dominik
'''
from IRCLibrary import IRC
print "MDSBot 0.2 initialized"
print "Using version " + IRC.version + " IRCLibrary"

import XmlHelper; print "Loading users..."
usrManager = XmlHelper.load_users()print "Loading settings..."
loadedSettings = XmlHelper.loadSettings()

import relay
relayManager = relay.relay_manager()

addresses = loadedSettings['addresses']
s = IRC.connection(addresses, loadedSettings['nicks'], \
        loadedSettings['realname'], loadedSettings['username'])
s.autojoinchans = loadedSettings['channels']

# Load the modules
print "Loading modules..."
loadedModules = {}
for module in loadedSettings['modules']:
    import imp, os, sys
    try:
        modulePath = os.path.join(os.path.dirname(sys.argv[0]), "modules/%s/%s.py" % (module, module))
        sys.path.append(os.path.dirname(modulePath))
        loadedModules[module] = imp.load_source(module, modulePath)
        loadedModules[module].main(s, "", usrManager)
        print "Module %s loaded." % (module)
    except IOError:
        #import traceback; traceback.print_exc()
        print "Error: module '%s' could not be found." % (module)

print "Initialization complete."

def main():
    import sys
    sys.path.append("modules")

    s.events.hook_event("QUIT", quit_logout)
    
    s.events.hook_event("PRIVMSG", privmsg)
    s.events.hook_event("disconnect", disconnect)

    print "Connecting..."
    s.connect(pingServ=False, threaded=False)

    # TODO: having .connect not calling .response would make more sense...

def disconnect(server, word, word_eol, args):
    import sys; sys.exit(1)
    
def privmsg(server, word, word_eol, args):
    import commands
    try:
        commands.cmd(server, word, word_eol, usrManager, relayManager, loadedModules)
    except:
        import traceback; traceback.print_exc()
    
def quit_logout(server, word, word_eol, args):
    usrManager.change_user_status(word[0].split("!")[0], False)
    
if __name__ == '__main__':
    main()
        
        
        
