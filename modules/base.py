#!/usr/bin/env python
'''
Example module
Take a look at the test module to check how events are handled.
'''

def main(server, initOnChannel, usrManager):
    # This gets called when the module is initialized.
    # InitOnChannel is the channel this module was loaded. Or nothing
    # if it was loaded at startup.

def destroy(server):
    # This gets called when the module get's unloaded.

def cmd(server, word, word_eol, usrManager):
    # This is called when a command is received(|cmd or |whatever)
