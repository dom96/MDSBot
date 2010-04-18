#!/usr/bin/env python
'''
Created on 2009-12-16

@author: Dominik
'''
from IRCLibrary import IRC
addresses = [["irc.freenode.net", 6667, "", False]]
s = IRC.server(addresses, ["MDSBot", "MDSBot_"], "MDSBot, MDS Net Bot", "MDSBot")

import XmlHelper
usrManager = XmlHelper.load_users()
factoidManager = XmlHelper.load_factoids()

import relay
relayManager = relay.relay_manager()

loadedModules = {}

def main():

    print "MDSBot 0.1 initialized"
    print "Using version " + IRC.version + " IRCLibrary"

    import sys
    sys.path.append("modules")

    s.events.hook_event("QUIT", quit_logout)
    

    s.events.hook_event("PRIVMSG", privmsg)
    s.events.hook_event("001", oper)
    s.connect(pingServ=False)

def disconnect(server, word, word_eol, args):
    pass
    
def privmsg(server, word, word_eol, args):
    import commands
    try:
        commands.cmd(server, word, word_eol, usrManager, relayManager, factoidManager, loadedModules)
    except:
        import traceback; traceback.print_exc()

def oper(server, word, word_eol, args):
    server.send("JOIN #()")
    
def quit_logout(server, word, word_eol, args):
    usrManager.change_user_status(word[0].split("!")[0], False)
    
if __name__ == '__main__':
    main()

    import time
    while True:
        time.sleep(10)
        
        
        
