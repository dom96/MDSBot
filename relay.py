'''
Created on 2009-12-18

@author: Dominik
'''
class relay_manager:
    def __init__(self):
        self.relays = []
        
    def add(self, relayToChan, chans, mainServer, address, port, nick, silent):
        """
        Adds a relay, relayToChan is the channel that 
        the !relay add command was executed, in other words the messages from chans
        will be relayed there.
        """
        newRelay = self.relay(self, relayToChan, chans, mainServer, address, port, nick, silent)
        self.relays.append(newRelay)
    
    def rem(self, index=None, addr="", quitMsg=""):
            try:
                if quitMsg != "":
                    #QUIT the server
                    self.get_relay(index, addr).server.send("QUIT :%s" % (quitMsg))
                
                relay = self.get_relay(index, addr)
                relay.unhookMainEvents()
                
                self.relays.remove(relay)
                return True
            except Exception as err:
                return err
        
    def get_relay(self, index=None, addr=""):
        if index != None:
            try:
                return self.relays[int(index)]
            except:
                return False
        elif addr != "":
            for i in self.relays:
                if i.server.address == addr:
                    return i
        
        return False
    
    class relay:
        def __init__(self, relay_man, relayToChan, chans, mainServer, address, port, nick, silent):
            from IRCLibrary import IRC
            self.server = IRC.server([[address, port, "", False]], [nick], nick, nick)
            self.server.autojoinchans = chans
            self.server.events.hook_event("PRIVMSG", lambda a,b,c,d: \
                                          relay_manager.privmsg(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("001", lambda a,b,c,d: \
                                          relay_manager.connected(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("JOIN", lambda a,b,c,d: \
                                          relay_manager.join(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("KICK", lambda a,b,c,d: \
                                          relay_manager.kick(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("PART", lambda a,b,c,d: \
                                          relay_manager.part(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("NICK", lambda a,b,c,d: \
                                          relay_manager.nick(relay_man, a, b, c, d), args=[self])
            self.server.events.hook_event("MODE", lambda a,b,c,d: \
                                          relay_manager.mode(relay_man, a, b, c, d), args=[self])

            self.server.events.hook_event("ERROR", lambda a,b,c,d: \
                                          relay_manager.disconnected(relay_man, a, b, c, d), args=[self])
            self.server.serverEvents.hook_event("disconnect", lambda a,b,c,d: \
                                          relay_manager.disconnected(relay_man, a, b, c, d), args=[self])


            self.mainServEventID = mainServer.events.hook_event("PRIVMSG", lambda a,b,c,d: \
                                          relay_manager.mainServer_privmsg(relay_man, a, b, c, d), args=[self])

            self.server.connect(pingServ=False)
            
            self.mainServer = mainServer
            self.relayToChan = relayToChan
            self.chans = chans
            self.silent = silent
            
        def unhookMainEvents(self):
            self.mainServer.events.unhook_event(self.mainServEventID)
            return True
            
    def connected(self, server, word, word_eol, args):
        args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, "\x0303Successfully connected to \x0301" + server.address))
                
    disconnectReason = ""
    def disconnected(self, server, word, word_eol, args):
        global disconnectReason
        if word[1] == "ERROR":
            disconnectReason = word[2]
        else:
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, "\x0305Disconnected from \x0301" \
                                                        + server.address + "\x0305(" + disconnectReason + ")"))
            self.rem(addr=server.address, quitMsg="")
        
    
    def join(self, server, word, word_eol, args):
        if word[0].split("!")[0] == server.nick and word[2].lower() in args[0].chans:
            #When you join the channel where the relay is meant to be
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, "\x0303Synced with \x0301" + word[2]))
        else:
            #Someone else joins
            if word[2].lower() in args[0].chans and args[0].relayToChan != word[2]:
                index = self.relays.index(args[0])
                msg = "\x0301[\x0305%s\x0301:\x0305%s\x0301]" % (index, word[2])
                msg += " " + "%s(\x0303%s\x0301)\x0303 joined" % (word[0].split("!")[0], word[0].split("!")[1])
            
                args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))
                
    def privmsg(self, server, word, word_eol, args):
        if word[2].lower() in args[0].chans and args[0].relayToChan != word[2].lower():
            index = self.relays.index(args[0])
            msg = "\x0301<\x0305%s\x0301:\x0305%s\x0301:\x0305%s\x0301>\x0301" % (word[0].split("!")[0], str(index), word[2])
            msg += " " + word[3]

            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))
            
    def kick(self, server, word, word_eol, args):
        if word[2] in args[0].chans and word[3] == server.nick:
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, \
                    "\x0305Kicked from \x0301" + word[2] + "\x0305 by \x0301" + word[0].split("!")[0]))
            args[0].server.send("JOIN %s" % (word[2]))
        else:
            #Someone else was kicked
            if word[2].lower() in args[0].chans and args[0].relayToChan != word[2].lower():
                index = self.relays.index(args[0])
                msg = "\x0301[\x0305%s\x0301:\x0305%s\x0301]" % (str(index), word[2])
                msg += " " + "%s \x0305was kicked by %s\x0301(\x0305%s\x0301)" % (word[3], word[0].split("!")[0], word[4])
            
                args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))
                
    def part(self, server, word, word_eol, args):
        if word[2].lower() in args[0].chans and args[0].relayToChan != word[2].lower():
            index = self.relays.index(args[0])
            partReason = ""
            if len(word) > 3:
                partReason = word[3]

            msg = "\x0301[\x0305%s\x0301:\x0305%s\x0301]" % (str(index), word[2])
            msg += " " + "%s \x0304left\x0301(\x0304%s\x0301)" % (word[0].split("!")[0], partReason)
        
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))

    def nick(self, server, word, word_eol, args):
        index = self.relays.index(args[0])
        msg = "\x0301[\x0305%s\x0301]" % (str(index))
        msg += " " + "%s is now known as %s" % (word[0].split("!")[0], word[2])
    
        args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))
        
    def mode(self, server, word, word_eol, args):
        if word[2].lower() in args[0].chans and args[0].relayToChan.lower() != word[2].lower() and \
                word[0] != args[0].server.nick:
            index = self.relays.index(args[0])
            msg = "\x0301[\x0305%s\x0301:\x0305%s\x0301]" % (str(index), word[2])
            if len(word) > 4:
                msg += " " + "%s\x0314 sets mode: \x0301%s\x0314 on \x0301%s" % (word[0].split("!")[0], word[3], word[4])
            else:
                msg += " " + "%s\x0314 sets mode: \x0301%s\x0314 on \x0301%s" % (word[0].split("!")[0], word[3], word[2])
        
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))
            
    def notice(self, server, word, word_eol, args):
        if word[2].lower() in args[0].chans and args[0].relayToChan.lower() != word[2].lower():
            index = self.relays.index(args[0])
            msg = "\x0301<\x0305%s\x0301:\x0305%s\x0301:\x0305%s\x0301>\x0307" % (word[0].split("!")[0], str(index), word[2])
            msg += " " + word[3]
        
            args[0].mainServer.send("PRIVMSG %s :%s" % (args[0].relayToChan, msg))

    """Main Server events start here"""
    def mainServer_privmsg(self, server, word, word_eol, args):
        if word[2].lower() == args[0].relayToChan.lower() and args[0].silent != True:
            msg = "\x0301<\x0305%s\x0301>\x0301" % (word[0].split("!")[0])
            msg += " " + word[3]
            
            for i in args[0].chans:
                if i != args[0].relayToChan:
                    args[0].server.send("PRIVMSG %s :%s" % (i, msg))
        
        
        