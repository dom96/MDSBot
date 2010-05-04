#!/usr/bin/env python
'''
Created on 2010-04-02

@author: Dominik
'''
about = "This module lets you download other modules from pastebin."
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|modules"):
        if word[3].split()[1] == "getpb":
            if usrManager.logged_in(word[0].split("!")[0], ["modules_getpb", "*"]):
                if len(word[3].split()) > 3:
                    pbName = word[3].split()[2]
                    moduleName = word[3].split()[3]

                    import os, os.path
                    if not os.path.exists("modules/" + moduleName):
                        os.mkdir("modules/" + moduleName)
                    else:
                        server.send("PRIVMSG " + word[2] + " :\x0305Module already exists")
                        return True

                    server.send("PRIVMSG " + word[2] + " :Downloading module from pastebin")
                    import urllib
                    urllib.urlretrieve("http://pastebin.com/download.php?i=" + pbName, \
                            "modules/" + moduleName + "/" + moduleName + ".py")
                    server.send("PRIVMSG " + word[2] + " :\x0303Module downloaded successfully")
            else:
                usrManager.print_insufficient_privils(word, server, "modules_getpb")
            return True
        elif word[3].split()[1] == "delete":
            if usrManager.logged_in(word[0].split("!")[0], ["modules_delete", "*"]):
                if len(word[3].split()) > 2:
                    name = word[3].split()[2]
                    if len(word[3].split()) < 4:
                        msg = "\x0305Please confirm by typing, \x02|modules delete " + name + " -c"
                        server.send("PRIVMSG " + word[2] + " :" + msg)
                        return True
                    else:
                        if word[3].split()[3] != "-c":
                            msg = "\x0305Please confirm by typing, \x02|modules delete " + name + " -c"
                            server.send("PRIVMSG " + word[2] + " :" + msg)
                            return True
                    
                    if name == "modulepb":
                        server.send("PRIVMSG " + word[2] + " :\x0305How dare you try to delete the almighty modulepb")
                        return True
                    import shutil, os.path
                    if os.path.exists("modules/" + name):
                        shutil.rmtree("modules/" + name)
                        server.send("PRIVMSG " + word[2] + " :\x0303Module deleted successfully")
                    else:
                        server.send("PRIVMSG " + word[2] + " :\x0305Module not found")
                    return True
            else:
                usrManager.print_insufficient_privils(word, server, "modules_delete")



