#!/usr/bin/env python
'''
Created on 2010-04-02

@author: Dominik
'''
eventHooks = []
def main(server, initOnChannel, usrManager):
    global eventHooks
    server.send("PRIVMSG " + initOnChannel + " :Test module initialized")
    eventHooks.append(server.events.hook_event("NOTICE", notice))
    

def destroy(server):
    global eventHooks
    for i in eventHooks:
        server.send("PRIVMSG #() :Unhooking event " + i)
        if server.events.unhook_event(i):
            server.send("PRIVMSG #() :" + i + " successfully unhooked.")
        else:
            server.send("PRIVMSG #() :" + i + " failed to unhooked.")

def notice(server, word, word_eol, args):
    server.send("PRIVMSG #() :NOTICE DETECTED")

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|test"):
        server.send("PRIVMSG %s :%s" % (word[2], "Test"))
        return True
