#!/usr/bin/env python
'''
Created on 2019-04-03

@author: Dominik
'''

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
            p = subprocess.Popen([os.path.dirname(os.path.realpath(__file__)) + "\\ael.exe"], \
                    stdout = subprocess.PIPE, stdin = subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate(code)
            for i in stdoutdata.split("\n"):
                if i != "":
                    server.send("PRIVMSG %s :%s" % (word[2], i))
            return True
