'''
Created on 2009-12-17

@author: Dominik
'''
import xml.dom.minidom
import os, sys

#USERS
def load_users(path=os.path.join(os.path.dirname(sys.argv[0]), "users.xml")):
    """Loads the users"""
    xmlDoc = xml.dom.minidom.parse(path)
    import users
    usrManager = users.user_manager()
    for userElement in xmlDoc.getElementsByTagName("user"):
        nick = getAttribute(userElement.attributes, "nick")
        import base64
        password = base64.b64decode(getAttribute(userElement.attributes, "password"))
        email = getAttribute(userElement.attributes, "email")
        privileges = getAttribute(userElement.attributes, "privileges")
        
        usrManager.add(nick, password, email, privileges.split(","))

        
    return usrManager
        
        
def save_users(user_manager, path=os.path.join(os.path.dirname(sys.argv[0]), "users.xml")):
    """Saves the users"""
    xmlDoc = xml.dom.minidom.parseString("<users></users>")
    
    for i in user_manager.users:
        userElement = xmlDoc.createElement("user")
        userElement.setAttribute("nick", i.nick)
        import base64
        userElement.setAttribute("password", base64.b64encode(i.password))
        userElement.setAttribute("privileges", ",".join(i.privileges))
        userElement.setAttribute("email", i.email)
        xmlDoc.documentElement.appendChild(userElement)
    
    f = open(path, "w")
    f.write(xmlDoc.toprettyxml(indent="    "))
    return True
    
#FACTOIDS
def load_factoids(path=os.path.join(os.path.dirname(sys.argv[0]), "factoids.xml")):
    """Loads the users"""
    xmlDoc = xml.dom.minidom.parse(path)
    import factoids
    factoidManager = factoids.factoid_manager()
    for factoidElement in xmlDoc.getElementsByTagName("factoid"):
        name = getAttribute(factoidElement.attributes, "name")
        #Get the contents
        for contentElement in factoidElement.getElementsByTagName("content"):
            factoidManager.add_factoid(name, str(getAttribute(contentElement.attributes, "content")))
        
    return factoidManager

def save_factoids(factoid_manager, path=os.path.join(os.path.dirname(sys.argv[0]), "factoids.xml")):
    """Saves the users"""
    xmlDoc = xml.dom.minidom.parseString("<factoids></factoids>")
    
    for i in factoid_manager.factoids:
        factoidElement = xmlDoc.createElement("factoid")
        factoidElement.setAttribute("name", i.name)
        print i.contents
        for content in i.contents:
            print content
            contentElement = xmlDoc.createElement("content")
            contentElement.setAttribute("content", content)

            factoidElement.appendChild(contentElement)
            
        xmlDoc.documentElement.appendChild(factoidElement)
    
    f = open(path, "w")
    f.write(xmlDoc.toprettyxml(indent="    "))
    return True

# Settings
def loadSettings(path=os.path.join(os.path.dirname(sys.argv[0]), "settings.xml")):
    """Loads the settings"""
    settings = {}

    xmlDoc = xml.dom.minidom.parse(path)

    settings['addresses'] = []
    for addressElement in xmlDoc.getElementsByTagName("address"):
        address = []
        address.append(getAttribute(addressElement.attributes, "host"))
        address.append(int(getAttribute(addressElement.attributes, "port")))
        address.append(getAttribute(addressElement.attributes, "pass"))
        address.append(getAttribute(addressElement.attributes, "ssl").lower() == "true")
        settings['addresses'].append(address)
    
    infoElement = xmlDoc.getElementsByTagName("info")[0]
    settings['nicks'] = getAttribute(infoElement.attributes, "nicks").split(",")
    settings['username'] = getAttribute(infoElement.attributes, "username")
    settings['realname'] = getAttribute(infoElement.attributes, "realname")
    settings['channels'] = getAttribute(infoElement.attributes, "channels").split(",")

    modulesElement = xmlDoc.getElementsByTagName("modules")[0]
    settings['modules'] = getAttribute(modulesElement.attributes, "load").split(",")

    return settings

def saveSettings(loadedModules, path=os.path.join(os.path.dirname(sys.argv[0]), "settings.xml")):
    xmlDoc = xml.dom.minidom.parse(path)

    xmlDoc.getElementsByTagName("modules")[0].setAttribute("load", ",".join(loadedModules.keys()))
    
    f = open(path, "w")
    f.write(xmlDoc.toprettyxml(indent="    "))
    return True    

"""getText, Get's the text of a tag"""
def getText(nodelist):
    txt = ""
    #Loop through the nodeList
    for node in nodelist:
        #If a TEXT_NODE is found add it to txt
        if node.nodeType == node.TEXT_NODE:
            txt = txt + node.data
    #And return it
    return txt
def getAttribute(attrlist, attrName):
    txt = ""
    #Loop through the attributes
    for i in range(0,attrlist.length):
        #If the attributes name == attrName
        if attrlist.item(i).nodeName == attrName:
            txt=attrlist.item(i).nodeValue
    #Then return the attributes value
    return txt
