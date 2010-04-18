#!/usr/bin/env python
'''
Created on 2019-04-08

@author: Dominik
'''

def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|op"):
        if len(word[3].split()) > 1:
            if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
                # Ask chanserv to op you.
                server.send("PRIVMSG ChanServ :%s" % ("OP " + word[3].split()[1]))
            else:
                usrManager.print_insufficient_privils(word, server, "op")
    
            return True

    if word[3].startswith("|deop"):
        if len(word[3].split()) > 1:
            if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
                # Ask chanserv to op you.
                server.send("PRIVMSG ChanServ :%s" % ("DEOP " + word[3].split()[1]))
            else:
                usrManager.print_insufficient_privils(word, server, "op")
    
            return True

    if word[3].startswith("|kick"):
        if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
            if len(word[3].split()) == 2:
                server.send("KICK %s %s" % (word[2], word[3].split()[1]))
            elif len(word[3].split()) > 2:
                server.send("KICK %s %s :%s" % (word[2], word[3].split()[1], server.gen_eol(word[3])[2]))
        else:
            usrManager.print_insufficient_privils(word, server, "op")

        return True

    if word[3].startswith("|ban"):
        if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
            if len(word[3].split()) > 1:
                server.send("MODE %s +b %s" % (word[2], word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "op")

    if word[3].startswith("|voice"):
        if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
            if len(word[3].split()) > 1:
                server.send("MODE %s +v %s" % (word[2], word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "op")

    if word[3].startswith("|devoice"):
        if usrManager.logged_in(word[0].split("!")[0], ["op", "*"]):
            if len(word[3].split()) > 1:
                server.send("MODE %s -v %s" % (word[2], word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "op")

        return True
