#!/usr/bin/env python
'''
Created at 04/05/10 16:20:31 
By Dominik Picheta
'''
import os.path, sys
import fClass
factoidManager = False
def main(server, initOnChannel, usrManager):
    global factoidManager
    factoidsDataPath = os.path.join(os.path.join(sys.path[0], \
        os.path.dirname(__file__)), "factoids.xml")
    try:
        factoidManager = fClass.load_factoids(factoidsDataPath)
    except IOError:
        if initOnChannel != '':
            server.send("PRIVMSG %s :%s" % (initOnChannel, "\x0305Couldn't load the factoids database."))

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    global factoidManager
    factoidsDataPath = os.path.join(os.path.join(sys.path[0], \
        os.path.dirname(__file__)), "factoids.xml")
    if word[3].startswith("|factoids"):
        if len(word[3].split()) > 1:
            if word[3].split()[1] == "add":
                if len(word[3].split()) > 3:
                        name = word[3].split()[2]
                        contents = " ".join(word[3].split()[3:])

                        factoidManager.add_factoid(name, contents)
                        fClass.save_factoids(factoidManager, factoidsDataPath)
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0303Factoid added!"))
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|factoids add name something..."))
                    
            if word[3].split()[1] == "rem":
                if len(word[3].split()) > 2:
                    if usrManager.logged_in(word[0].split("!")[0], ["factoids_rem", "*"]):
                        name = word[3].split()[2]                 

                        factoidManager.rem_factoid(name)
                        fClass.save_factoids(factoidManager, factoidsDataPath)
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0303Factoid removed!"))
                    else:
                        usrManager.print_insufficient_privils(word, server, "factoids_rem")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|factoids rem name"))
                    
            if word[3].split()[1] == "get":
                if len(word[3].split()) > 2:
                        name = word[3].split()[2]

                        fact = factoidManager.get_factoid(name)
                        if fact != False:
                            msg = "\x0307" + name + " \x0314is\x03 "
                            for i in range(len(fact.contents)):
                                if i == len(fact.contents) - 1:
                                    msg += fact.contents[i]
                                elif i == len(fact.contents) - 2:
                                    msg += fact.contents[i] + " \x0314and also is\x0301 "
                                else:
                                    msg += fact.contents[i] + "\x0314, \x0301"
                            server.send("PRIVMSG %s :%s" % (word[2], msg))
                            
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0305Factoid not found"))

                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|factoids add name something..."))
            
            
        else:
            server.send("PRIVMSG %s :%s" % (word[2], "|factoids [add/rem/get]"))
        return True
