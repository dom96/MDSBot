'''
Created on 2009-12-17

@author: Dominik
'''
class user_manager:
    def __init__(self):
        self.users = []
    
    def rem(self, nick):
        for usr in self.users:
            if usr.nick == nick:
                self.users.remove(usr)
                return True
            
        return False
    
    def add(self, nick, password, email, privileges=["default"]):
        newUsr = self.user(nick, privileges, email, password)
        self.users.append(newUsr)
        
    def modify_privil(self, nick, privilege, delete=False):
        user = self.get_user(nick)
        if user != False:
            if delete == False:
                user.privileges.append(privilege)
            else:
                try:
                    user.privileges.remove(privilege)
                except:
                    return False
        return False
                    
    def logged_in(self, nick, privilege):
        """
        Checks if the user is logged in
        And if he/she/it has the privileges specified
        If you specify "" for the privileges, 
        then this function will return true if the user is logged in
        
        privilege can be a string or a list
        """
        user = self.get_user(nick)
        if user != False:
            if user.loggedIn == True:
                if privilege != "":
                    return self.has_privil(nick, privilege)
                else:
                    return True
                    
        return False
                
    def has_privil(self, nick, privilege):
        user = self.get_user(nick)
        if user != False:
            for i in user.privileges:
                if i == privilege or i in privilege:
                    return True
                
        return False
                    
    def change_user_status(self, nick, status):
        user = self.get_user(nick)
        if user != False:
            user.loggedIn = status
            return True
        else:
            return False
                    
    def get_user(self, nick):
        for usr in self.users:
            if usr.nick.lower() == nick.lower():
                return usr
            
        return False
    
    def print_insufficient_privils(self, word, server, privilNeeded=""):
        if privilNeeded != "":
            server.send("PRIVMSG %s :%s" % (word[2], \
                             "\x0305You have insufficient privileges to use this command, you need the " + privilNeeded + " privilege." ))
        else:
            server.send("PRIVMSG %s :%s" % (word[2], "\x0305You have insufficient privileges to use this command"))
        
    class user:
        def __init__(self, nick, privilages, email, password):
            self.nick = nick
            self.password = password
            self.privileges = privilages
            self.email = email
            self.loggedIn = False
            
