#!/usr/bin/env python
'''
Created on 09/05/10 22:46:55 
By Dominik Picheta
'''
about = "This module allows you to give a question and an answer. Which people in a channel can then answer with |answer answer here"

question = ""
answer = ""

def main(server, initOnChannel, usrManager):
    pass

def destroy(server):
    pass

def cmd(server, word, word_eol, usrManager):
    global question
    global answer
    if word[3].startswith("|?") and len(word[3].split()) > 1:
        question = server.gen_eol(word[3])[1]
        server.send("PRIVMSG %s :%s" % (word[2], \
                "Send me the answer with /msg MDSBot |answer Answer to question here"))
        return True
    elif word[3].startswith("|answer") and len(word[3].split()) > 1:
        if question != "" and answer == "":
            answer = server.gen_eol(word[3])[1]
            server.send("PRIVMSG %s :%s" % (word[2], \
                    "Question accepted"))
        elif question != "" and answer != "":
            if server.gen_eol(word[3])[1] == answer:
                server.send("PRIVMSG %s :%s" % (word[2], \
                        "\x0303Correct!"))
                question = ""; answer = ""
            else:
                server.send("PRIVMSG %s :%s" % (word[2], \
                        "\x0305Wrong answer"))
        elif question == "":
            server.send("PRIVMSG %s :%s" % (word[2], \
                    "No question asked."))

        return True



