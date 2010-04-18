#!/usr/bin/env python
'''

Created on 2010-04-02



@author: Dominik

'''
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|all your base"):
        server.send("PRIVMSG %s :%s" % (word[2], "are belong to us"))
        return True