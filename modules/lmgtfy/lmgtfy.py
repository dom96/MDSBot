#!/usr/bin/env python
'''
Created on 2019-04-06

@author: Dominik
'''

def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|lmgtfy"):
        if len(word[3].split()) > 1:
            search = server.gen_eol(word[3])[1]
            import urllib
            server.send("PRIVMSG %s :%s" % (word[2], "http://lmgtfy.com/?q=" + urllib.quote_plus(search)))
            return True
