#!/usr/bin/env python
'''
Created on 06/05/10 15:48:42
By Dominik Picheta
'''
import sgC
players = []
about = "An IRC Space Game similar to ogame."
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    # Stop the players
    global players
    for i in players:
        i.running = False

    # reload sgC so that |modules reload works
    reload(sgC)

def get_player(nick):
    global players
    for i in players:
        if i.nick == nick:
            return i

    return False

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|sg register"):
        if len(word[3].split()) > 3:
            if usrManager.logged_in(word[0].split("!")[0], ""):
                race = word[3].split()[3]
                if race == "opran": race = sgC.OPRAN_RACE
                elif race == "elders": race = sgC.ELDERS_RACE
                elif race == "lok": race = sgC.LOK_RACE
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "\x0305Invalid race."))
                    return True
                
                emp = sgC.empire(word[3].split()[2], race)
                player = sgC.player(word[0].split("!")[0], emp)
                emp.player = player
                emp.start()

                global players
                players.append(player)
                server.send("PRIVMSG %s :%s" % (word[2], "\x0303You are now in the game!"))
                return True
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "\x0305To play you need to be logged in."))
                return True
            
        else:
            server.send("PRIVMSG %s :%s" % (word[2], "Usage: |sg register EmpireName Race"))
            server.send("PRIVMSG %s :%s" % (word[2], "For more information, |sg help register"))
            return True

    elif word[3].startswith("|sg build") and word[3].split()[1] == "build":
        if len(word[3].split()) > 2:
            if usrManager.logged_in(word[0].split("!")[0], ""):
                buildID = int(word[3].split()[2])
                if buildID > 2:
                    server.send("PRIVMSG %s :%s" % (word[2], "\x0305Wrong building ID"))
                    return True

                player = get_player(word[0].split("!")[0])
                if player != False:
                    resp = player.empire.planets[0].build_building(buildID)
                    if resp == True:
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0303Your building is being built."))
                    else:
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0305" + resp))
                    return True
                    
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "\x0305You must have an empire to build."))
                    return True
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "\x0305To play you need to be logged in."))
                return True

        else:
            server.send("PRIVMSG %s :%s" % (word[2], "Usage: |sg build building_id"))
            server.send("PRIVMSG %s :%s" % (word[2], "For more information and to see available buildings, |sg help build"))
            return True

    elif word[3].startswith("|sg resources"):
        if usrManager.logged_in(word[0].split("!")[0], ""):
            player = get_player(word[0].split("!")[0])
            if player != False:
                titanium = player.empire.planets[0].titanium
                gallium = player.empire.planets[0].gallium
                hydrogen = player.empire.planets[0].hydrogen
                server.send("PRIVMSG %s :%s" % (word[2], \
                    "Titanium: %s Gallium: %s Hydrogen: %s" % (titanium, gallium, hydrogen)))
                return True
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "\x0305You must have an empire to play."))
                return True

        else:
            server.send("PRIVMSG %s :%s" % (word[2], "\x0305To play you need to be logged in."))
            return True

    elif word[3].startswith("|sg buildings"):
        if usrManager.logged_in(word[0].split("!")[0], ""):
            player = get_player(word[0].split("!")[0])
            if player != False:
                msg = "Buildings: "
                for i in player.empire.planets[0].buildings:
                    msg += sgC.get_building_name(i.buildingID) + " Level " + str(i.level)

                server.send("PRIVMSG %s :%s" % (word[2], msg))
                return True
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "\x0305You must have an empire to play."))
                return True

        else:
            server.send("PRIVMSG %s :%s" % (word[2], "\x0305To play you need to be logged in."))
            return True

    elif word[3].startswith("|sg queue"):
        if usrManager.logged_in(word[0].split("!")[0], ""):
            player = get_player(word[0].split("!")[0])
            if player != False:
                if len(player.empire.planets[0].queue) != 0:
                    msg = "queue: "
                    for i in player.empire.planets[0].queue:
                        if i.item.__class__ == sgC.building:
                            import time
                            s = i.timestamp - time.time()
                            
                            days, remainder = divmod(s, 1440)
                            hours, remainder = divmod(remainder, 3600)
                            minutes, seconds = divmod(remainder, 60)

                            msg += sgC.get_building_name(i.item.buildingID) + " Level " + str(i.item.level)
                            msg += "\x0314[\x0301" + "%s:%s:%s:%s" % (int(days), int(hours), int(minutes), int(seconds)) + "\x0314]\x03"

                    server.send("PRIVMSG %s :%s" % (word[2], msg))
                else:
                    server.send("PRIVMSG %s :%s" % (word[2], "Nothing in the queue"))
                return True
            else:
                server.send("PRIVMSG %s :%s" % (word[2], "\x0305You must have an empire to play."))
                return True

        else:
            server.send("PRIVMSG %s :%s" % (word[2], "\x0305To play you need to be logged in."))
            return True


    elif word[3].startswith("|sg help"):
        if len(word[3].split()) > 2:
            topic = word[3].split()[2]
            player = get_player(word[0].split("!")[0])
            if topic == "register":
                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "This command lets you register an sg empire. " + \
                    "Please note you have to be registered(and identified) with MDSBot for this to work."))
            elif topic == "race":
                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "When registering you have to choose a race. " + \
                    "Each race has a bonus and each race can only " + \
                    "sustain life on a particular type of planet."))

                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "There are 3 races: the opran, the elders and the lok. Use |sg help race" + \
                    " to learn more about each race."))
            elif topic == "opran":
                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "The opran are creatures which breathe Carbon Dioxide"))
            elif topic == "elders":
                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "The elders are ancient creatures which breathe oxygen"))
            elif topic == "lok":
                server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                    "The lok are creatures which breathe Nitrogen"))
            elif topic == "build":
                if player != False:
                    server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                        "Build lets you build buildings. Buildings currently" + \
                        " available to build are:"))

                    TM = player.empire.planets[0].get_building(0)
                    if TM == None: TM = sgC.building(0, player.empire.planets[0])

                    TMTitanium, TMGallium, TMHydrogen = sgC.calculate_build_resources(TM)
                    server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                            "Titanium Mine [0] - Titanium: %s Gallium: %s Hydrogen: %s" % ( \
                             TMTitanium, TMGallium, TMHydrogen)))

                    GM = player.empire.planets[0].get_building(1)
                    if GM == None: GM = sgC.building(1, player.empire.planets[0])

                    GMTitanium, GMGallium, GMHydrogen = sgC.calculate_build_resources(GM)
                    server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                            "Gallium Mine [1] - Titanium: %s Gallium: %s Hydrogen: %s" % ( \
                             GMTitanium, GMGallium, GMHydrogen)))

                    HS = player.empire.planets[0].get_building(2)
                    if HS == None: HS = sgC.building(2, player.empire.planets[0])         

                    HSTitanium, HSGallium, HSHydrogen = sgC.calculate_build_resources(HS)
                    server.send("NOTICE %s :%s" % (word[0].split("!")[0], \
                            "Hydrogen Synthesizer [2] - Titanium: %s Gallium: %s Hydrogen: %s" % ( \
                             HSTitanium, HSGallium, HSHydrogen)))
                else:
                    server.send("NOTICE %s :%s" % (word[0].split("!")[0], "This command let's you build."))

            return True


        else:
            server.send("PRIVMSG %s :%s" % (word[2], "Usage: |sg help \x02topic\x02"))
            return True


