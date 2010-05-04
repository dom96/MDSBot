#!/usr/bin/env python
'''
Created on 2019-04-09

@author: Dominik
'''
about = "A 'half-assed' wiki module."
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|wiki"):
        if len(word[3].split()) > 1:
            search = server.gen_eol(word[3])[1]

            server.send("PRIVMSG %s :%s" % (word[2], "http://en.wikipedia.org/wiki/" + search))
            return True
