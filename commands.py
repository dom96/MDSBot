#!/usr/bin/env python
'''
Created on 2009-12-16

@author: Dominik
'''
import XmlHelper
def cmd(server, word, word_eol, usrManager, relayManager, loadedModules):
    # if this is not a PRIVMSG to a channel make word[2] the nick of the
    # person that is sending this.
    if word[2] == server.nick:
        word[2] = word[0].split("!")[0]
    
    

    
    if word[3] == "|about":
        aboutMsg = "MDSBot 0.2 :D"
        server.send("PRIVMSG %s :%s" % (word[2], aboutMsg))
        return True
        
    elif word[3] == "VERSION":
        server.send("NOTICE %s :%s" % (word[0].split("!")[0], "VERSION MDSBot 0.2 :D"))
        return True
        
    elif word[3].startswith("|quit"):
        if usrManager.logged_in(word[0].split("!")[0], "quit") \
         or usrManager.logged_in(word[0].split("!")[0], "*"):
            quitMsg = "Quitting on request of " + word[0].split("!")[0]
            
            if len(word[3].split()) > 1:
                quitMsg = server.gen_eol(word[3])[1]
            
            #Quit the relays(remove them)
            for i in range(len(relayManager.relays)):
                relayManager.rem(i, quitMsg=quitMsg)
            
            server.send("QUIT :%s" % (quitMsg))
        else:
            usrManager.print_insufficient_privils(word, server, "quit")
        return True
    
    elif word[3].startswith("|say"):
        if usrManager.logged_in(word[0].split("!")[0], ["say", "*"]):
            chann = word[2]
            msg = server.gen_eol(word[3])[1]
            if word[3].split()[1].startswith("#"):
                chann = word[3].split()[1]
                msg = server.gen_eol(word[3])[2]

            server.send("PRIVMSG %s :%s" % (chann, msg))
        else:
            usrManager.print_insufficient_privils(word, server, "say")

        return True
    
    ##########################################################################
    #                                USERS                                   #
    elif word[3].startswith("register") and (word[2].startswith("#") == False):
        if len(word[3].split()) > 1:
            nick = word[0].split("!")[0]
            password = word[3].split()[1]
            email = word[3].split()[2]
        else:
            reply = "register: \x02register password email"
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], reply))
            return True
            
        #Check if there already is a user by this nick
        if usrManager.get_user(nick) == False:
            usrManager.add(nick, password, email)

            XmlHelper.save_users(usrManager)
            #Send a message confirming.
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "You have registered successfully"))
        else:
            reply = "An account for " + nick + " already exists."
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], reply))
            
        return True
            
    elif word[3].startswith("identify") and (word[2].startswith("#") == False):
        #Check if the user didn't just say identify
        if len(word[3].split()) > 1:
            nick = word[0].split("!")[0]
            password = word[3].split()[1]
        else:
            reply = "Identify: \x02identify password"
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], reply))
            return True
        
        user = usrManager.get_user(nick)
        if user != False:
            #Check if the password is correct
            if user.password == password:
                usrManager.change_user_status(nick, True)
                #Send a message confirming.
                server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "You are now identified as \x02" + nick))
            else:
                server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "\x0305Incorrect password"))
        else:
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "\x0305No user by this nickname found"))
        
        return True
    
    elif word[3].startswith("logout") and (word[2].startswith("#") == False):
        #Check if the user didn't just say logout
        if len(word[3].split()) > 2:
            nick = word[3].split()[1]
            password = word[3].split()[2]
            
            user = usrManager.get_user(nick)
            if user != False:
                #Check if the password is correct
                if user.password == password:
                    usrManager.change_user_status(nick, False)
                    #Send a message confirming.
                    server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "\x02" + nick + "\x02 is now logged out"))
                else:
                    server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "\x0305Incorrect password"))
                
            else:
                server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], "\x0305User doesn't exist"))
            
        else:
            reply = "logout: \x02logout nick password"
            server.send("PRIVMSG %s :%s" % (word[0].split("!")[0], reply))
        
        return True
    
    elif word[3].startswith("|privileges"):
        if usrManager.logged_in(word[0].split("!")[0], ""):
            user = usrManager.get_user(word[0].split("!")[0])
            
            server.send("PRIVMSG %s :%s" % (word[2],"Your privileges are \x0307" + ", ".join(user.privileges)))
        else:
            server.send("PRIVMSG %s :%s" % (word[2], \
            "\x0305You don't have any privileges because your not logged in."))
        return True

    
    elif word[3].startswith("|user") and len(word[3].split()) > 3:
        if word[3].split()[2] == "privileges":
            #Check if the user exists
            user = usrManager.get_user(word[3].split()[1])
            if user == False:
                server.send("PRIVMSG %s :%s" % (word[2], \
                "\x0305User doesn't exist"))
                return True
                
            if len(word[3].split()) > 4:    
                #Adds privileges to a user
                if word[3].split()[3] == "add":
                    #Check if the user is logged in and has privileges
                    if usrManager.logged_in(word[0].split("!")[0], ["user_privils_add", "*"]) \
                     and usrManager.has_privil(word[0].split("!")[0], [word[3].split()[4], "*"]):
                        user = usrManager.modify_privil(word[3].split()[1], word[3].split()[4])
                        XmlHelper.save_users(usrManager)
                        server.send("PRIVMSG %s :%s" % (word[2], \
                                    "\x0303Privileges for \x0307" + word[3].split()[1] + " \x0303added successfully"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "user_privils_add")
                    
                    return True
                    
                #Removes privileges from a user
                elif word[3].split()[3] == "rem":
                    #Check if the user is logged in and has privileges
                    #Also check if the user from who you want to remove privileges doesn't have *
                    if usrManager.logged_in(word[0].split("!")[0], ["user_privils_rem", "*"]) \
                        and (usrManager.has_privil(word[3].split()[1], "*") == False \
                             or usrManager.has_privil(word[0].split("!")[0], "*")):
                        user = usrManager.modify_privil(word[3].split()[1], word[3].split()[4], True)
                        XmlHelper.save_users(usrManager)
                        server.send("PRIVMSG %s :%s" % (word[2], \
                                    "\x0303Privileges for \x0307" + word[3].split()[1] + " \x0303removed successfully"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "user_privils_rem")
                    
                    return True
                    
            #Lists users privileges
            if word[3].split()[3] == "list":
                #Check if the user is logged in and has privileges
                if usrManager.logged_in(word[0].split("!")[0], ["user_privils_list", "*"]):
                    user = usrManager.get_user(word[3].split()[1])
                    server.send("PRIVMSG %s :%s" % (word[2], \
                                word[3].split()[1] + " privileges are \x0307" + ", ".join(user.privileges)))
                    
                else:
                    usrManager.print_insufficient_privils(word, server, "user_privils_list")
                    
            #If the command is incorrect, print the help        
            else:
                print_user_help(word, server)
                    
        #Print the help if the command is incorrect
        else:
            print_user_help(word, server)
        
        return True
    
    elif word[3].startswith("|users"):
        if usrManager.logged_in(word[0].split("!")[0], ["list_users", "*"]):
            loggedInUsers = []
            for usr in usrManager.users:
                if usr.loggedIn:
                    loggedInUsers.append(usr.nick)
                    
            msg = ", ".join(loggedInUsers)
            server.send("PRIVMSG %s :%s" % (word[2], "Users that are logged in: " + msg))
        else:
            usrManager.print_insufficient_privils(word, server, "list_users")
        
        return True
    
    elif word[3].startswith("|user"): print_user_help(word, server); return True
    
            
    #                USERS END                #
    ###########################################
    #                RELAY START              #
    
    elif word[3].startswith("|relay"):
        try:
            if word[3].split()[1] == "add":
                if len(word[3].split()) > 3:
                    if usrManager.logged_in(word[0].split("!")[0], ["relay", "*"]):
                        addr = word[3].split()[2]
                        chan = word[3].split()[3]
                        port = 6667
                        relayToChan = word[2]
                        nick = "MDSBot"
                        silent = True
                        if len(word[3].split()) > 4:
                            port = int(word[3].split()[4])
                        if len(word[3].split()) > 5:
                            relayToChan = word[3].split()[5]
                        if len(word[3].split()) > 6:
                            nick = word[3].split()[6]
                        if len(word[3].split()) > 7:
                            if word[3].split()[7] == "t": silent = True
                            if word[3].split()[7] == "f": silent = False
                            
                        #Join relayToChan
                        server.send("JOIN %s" % (relayToChan))                            
                            
                        #Check if a relay with this address already exists
                        if relayManager.get_relay(addr=addr) == False:
                            relayManager.add(relayToChan.lower(), [chan.lower()], server, addr, port, nick, silent)
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], \
                                            "\x0305A relay which is connected to \x0301" + addr + " \x0305already exists."))
                            return True
                        
                        server.send("PRIVMSG %s :%s" % (word[2], "Connecting to %s:%s/%s" % (addr, port, chan)))
                    else:
                        usrManager.print_insufficient_privils(word, server, "relay")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|relay add server #chan [port] [#relayToChan] [nick] [silent(t/f)]"))

            elif word[3].split()[1] == "rem":
                if len(word[3].split()) > 2:
                    if usrManager.logged_in(word[0].split("!")[0], ["relay", "*"]):
                        index = word[3].split()[2] #This is either the index or the address
                        
                        if "." in index:
                            result = relayManager.rem(addr=index, quitMsg="Relay terminated")
                        else:
                            result = relayManager.rem(index, quitMsg="Relay terminated")
                        
                        if result == True:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0303Relay removed"))
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0305Error removing relay"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "relay")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|relay rem index/address"))
                    
            elif word[3].split()[1] == "info":
                if len(word[3].split()) > 2:
                    if usrManager.logged_in(word[0].split("!")[0], ["default", "*"]):
                        index = word[3].split()[2] #This is either the index or the address
                        relay = relayManager.get_relay(index)
                        if "." in index:
                            relay = relayManager.get_relay(addr=index)
                            
                        if relay != False:
                            message = "\x0305Address: \x0304%s \x0305Port: \x0304%s " % \
                                (relay.server.address, str(relay.server.port))
                            message += "\x0305Channel(s): \x0304%s \x0305Relays to channel: \x0304%s \x0305Nick: \x0304%s \x0305Silent: \x0304%s" % \
                                (", ".join(relay.chans), relay.relayToChan, relay.server.nick, relay.silent)
                            
                            server.send("PRIVMSG %s :%s" % (word[2], message))
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0305Error retrieving relay info"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "relay")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|relay info index/address"))
                    
            elif word[3].split()[1] == "join":
                if len(word[3].split()) > 3:
                    if usrManager.logged_in(word[0].split("!")[0], ["relay", "*"]):
                        index = word[3].split()[2] #This is either the index or the address
                        chan = word[3].split()[3]
                        relay = relayManager.get_relay(index)
                        if "." in index:
                            relay = relayManager.get_relay(addr=index)
                        if relay != False:
                            relay.chans.append(chan.lower())
                            relay.server.send("JOIN %s" % chan)
                            
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0303Joining " + chan))
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0305Error relay could not be found"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "relay")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|relay join index/address #chan"))
                    
            elif word[3].split()[1] == "part":
                if len(word[3].split()) > 3:
                    if usrManager.logged_in(word[0].split("!")[0], ["relay", "*"]):
                        index = word[3].split()[2] #This is either the index or the address
                        chan = word[3].split()[3]
                        relay = relayManager.get_relay(index)
                        if "." in index:
                            relay = relayManager.get_relay(addr=index)
                            
                        if relay != False:
                            
                            if chan in relay.chans:
                                relay.chans.remove(chan.lower())
                                relay.server.send("PART %s" % chan)
                                
                                server.send("PRIVMSG %s :%s" % (word[2], "\x0303Leaving " + chan))
                            else:
                                server.send("PRIVMSG %s :%s" % (word[2], "\x0305The relay isn't in that channel"))
                            
                            
                        else:
                            server.send("PRIVMSG %s :%s" % (word[2], "\x0305Error relay could not be found"))
                        
                    else:
                        usrManager.print_insufficient_privils(word, server, "relay")
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "|relay part index/address #chan"))
                    
            else: server.send("PRIVMSG %s :%s" % (word[2], "|relay add server #chan [port] [nick] [silent(t/f)]"))
                    
            
        except Exception as err:
            print str(err)
            server.send("PRIVMSG %s :%s" % (word[2], "|relay [add/info/rem/join/part]"))
                
        return True
    
    #    RELAY END   #
    ##################
    # FACTOIDS START #

    elif word[3].startswith("|join") and len(word[3].split()) > 1:
        if usrManager.logged_in(word[0].split("!")[0], ["join", "*"]):
            server.send("JOIN %s" % (word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "join")
        return True
    
    elif word[3].startswith("|part") and len(word[3].split()) > 1:
        if usrManager.logged_in(word[0].split("!")[0], ["part", "*"]):
            server.send("PART %s" % (word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "part")
        return True

    elif word[3].startswith("|nick") and len(word[3].split()) > 1:
        if usrManager.logged_in(word[0].split("!")[0], ["nick", "*"]):
            server.send("NICK %s" % (word[3].split()[1]))
        else:
            usrManager.print_insufficient_privils(word, server, "nick")
        return True   

    elif word[3].startswith("|modules"):
        if word[3].split()[1] == "load":
            if usrManager.logged_in(word[0].split("!")[0], ["modules_load", "*"]):
                if len(word[3].split()) > 2:
                    name = word[3].split()[2]
                    
                    import imp, os, sys
                    try:
                        modulePath = os.path.join(os.path.dirname(sys.argv[0]), "modules/%s/%s.py" % (name, name))
                        sys.path.append(os.path.dirname(modulePath))
                        loadedModules[name] = imp.load_source(name, modulePath)
                        loadedModules[name].main(server, word[2], usrManager)
                        XmlHelper.saveSettings(loadedModules)
                    except IOError:
                        import traceback;traceback.print_exc()
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0305Module not found"))

            else:
                usrManager.print_insufficient_privils(word, server, "modules_load")
    
            return True

        elif word[3].split()[1] == "unload":
            if usrManager.logged_in(word[0].split("!")[0], ["modules_unload", "*"]):
                if len(word[3].split()) > 2:
                    name = word[3].split()[2]
                    try:
                        loadedModules[name].destroy(server)
                        del loadedModules[name]
                        modulePath = os.path.join(os.path.dirname(sys.argv[0]), "modules/%s/%s.py" % (name, name))
                        import sys; sys.path.remove(sys.path.index(os.path.dirname(modulePath)))
                        XmlHelper.saveSettings(loadedModules)
                    except KeyError:
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0305Module not found"))

            else:
                usrManager.print_insufficient_privils(word, server, "modules_unload")
            return True

        elif word[3].split()[1] == "reload":
            if usrManager.logged_in(word[0].split("!")[0], ["modules_load", "*"]):
                if len(word[3].split()) > 2:
                    name = word[3].split()[2]
                    
                    try:
                        # Unload the module
                        loadedModules[name].destroy(server)
                        del loadedModules[name]

                        # Load the module
                        import imp, os, sys
                        loadedModules[name] = imp.load_source(name, \
                            os.path.join(os.path.dirname(sys.argv[0]), "modules/%s/%s.py" % (name, name)))
                        loadedModules[name].main(server, word[2], usrManager)

                        XmlHelper.saveSettings(loadedModules)
                    except KeyError:
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0305Module not found"))
                        return True

                    return True


        elif word[3].split()[1] == "list":
            if len(loadedModules.keys()) != 0:
                server.send("PRIVMSG %s :%s" % (word[2], "Currently loaded modules: " + \
                        ", ".join(loadedModules.keys())))
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "There are no loaded modules"))

            return True

        elif word[3].split()[1] == "about":
            if len(word[3].split()) > 2:
                name = word[3].split()[2]
                try:
                    server.send("PRIVMSG %s :%s" % (word[2], loadedModules[name].about))
                except KeyError:
                    server.send("PRIVMSG %s :%s" % (word[2], "\x0305Module not found"))
                except AttributeError:
                    server.send("PRIVMSG %s :%s" % (word[2], "\x0305Module has no about message."))
                return True

    # Call the modules .cmd
    for i in iter(loadedModules):
        try:
            if loadedModules[i].cmd(server, word, word_eol, usrManager):
                return True
        except:
            # Print the error...
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()

            error = traceback.extract_tb(exc_traceback)
            msg = "\x0305Error, line: %s at function \'%s\'" % \
                (error[len(error)-1][1], error[len(error)-1][2])
            msg2 = "    " + error[len(error)-1][3]
            server.send("PRIVMSG %s :%s" % (word[2], msg))
            server.send("PRIVMSG %s :%s" % (word[2], "    " + str(exc_value)))
            server.send("PRIVMSG %s :%s" % (word[2], msg2))

            return True

    if word[3].startswith("|"):
        server.send("PRIVMSG %s :%s" % (word[2], "\x0305Unknown command"))

    return True
















def print_user_help(word, server):
    userHelp = "|user \x02nick\x02 privileges add \x02privilege\n"
    userHelp += "     Gives a privilege to a user\n"
    userHelp += "|user \x02nick\x02 privileges rem \x02privilege\n"
    userHelp += "     Removes a privilege from a user"
    for i in userHelp.split("\n"):
        server.send("NOTICE %s :%s" % (word[0].split("!")[0], i))
    
    
