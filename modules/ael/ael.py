#!/usr/bin/env python
'''
Created on 2019-04-03

@author: Dominik
'''
about = "This module implements the AEL(Awesome Esoteric Language) interpreter"
def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    if word[3].startswith("|ael"):
        if len(word[3].split()) > 1:
            code = server.gen_eol(word[3])[1]
            import os, os.path
            
            import subprocess
            path = ""
            if os.name == "posix":
                path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ael")
            elif os.name == "nt":
                path = os.path.dirname(os.path.realpath(__file__)) + "\\ael.exe"

            
            p = subprocess.Popen([path], \
                    stdout = subprocess.PIPE, stdin = subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate(code)
            for i in stdoutdata.split("\n"):
                if i != "":
                    server.send("PRIVMSG %s :%s" % (word[2], i))
            return True
