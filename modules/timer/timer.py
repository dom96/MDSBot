#!/usr/bin/env python
'''
Created on 2019-04-10

@author: Dominik
'''
timers = [] # seconds when the timer ends.., message
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def timerEnd(server, chan, msg, time):
    global timers
    try:
        del timers[timers.index([time, msg])]
        fMsg = msg
        # Make /me into an action :P
        if msg.startswith("/me"):
            fMsg = fMsg.replace("/me", "\x01ACTION") + "\x01"

        server.send("PRIVMSG %s :%s" % (chan, fMsg))
    except:
        pass

def cmd(server, word, word_eol, usrManager):
    global timers
    if len(word[3].split()) > 1:
        if word[3].split()[0] == "|timer":
            if len(word[3].split()) > 2:
                if word[3].split()[1] != "del":
                    try:
                        hour = int(word[3].split()[1].split(":")[0])
                        minute = int(word[3].split()[1].split(":")[1])
                        second = int(word[3].split()[1].split(":")[2])
                    except:
                        return False

                    msg = server.gen_eol(word[3])[2]
                    import threading, time
                    t = (hour * 3600 + minute * 60 + second)
                    timers.append([int(time.time() + t), msg])
                    t = threading.Timer(t, timerEnd, [server, word[2], msg, int(time.time() + t)])
                    t.start()

                    return True
                else:
                    try:
                        del timers[int(word[3].split()[2])]
                    except:
                        server.send("PRIVMSG %s :%s" % (word[2], "\x0305Timer not found\x03"))
                    return True


            else:
                server.send("PRIVMSG %s :%s" % (word[2], "Syntax: |timer hh:mm:ss \x0305>\x03msg\x0305<\x03"))
                server.send("PRIVMSG %s :%s" % (word[2], "Syntax: |timer del \x0305>\x03id\x035<\x03"))
                return True

    if word[3].startswith("|timers"):
        if len(timers) != 0:
            import time
            msg = "Running timers: "
            for i in timers:
                s = i[0] - time.time()
                # http://stackoverflow.com/questions/538666/python-format-timedelta-to-string
                hours, remainder = divmod(s, 3600)
                minutes, seconds = divmod(remainder, 60)

                msg += "\x0305[\x0301" + str(timers.index([i[0], i[1]])) + "\x0305]\x0302" + "%s:%s:%s" % \
                    (int(hours), int(minutes), int(seconds)) + "\x03 - " + i[1][:15] + "..."
                if timers.index(i) != len(timers)-1:
                    msg += ", "

            server.send("PRIVMSG %s :%s" % (word[2], msg))
        else:
            server.send("PRIVMSG %s :%s" % (word[2], "No running timers."))

        return True



