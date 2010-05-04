#!/usr/bin/env python
'''
Created on 2009-12-31

@author: Dominik
'''
class factoid_manager():
    def __init__(self):
        self.factoids = []
        
    def add_factoid(self, name, contents):
        fact = self.get_factoid(name)
        if fact == False:
            fact = self.factoid(name, contents)
            self.factoids.append(fact)
        else:
            fact.contents.append(contents)
    
    def rem_factoid(self, name, index=None):
        fact = self.get_factoid(name)
        if fact != False:
            if index == None:
                self.factoids.remove(fact)
            else:
                try:
                    fact.contents.remove(fact.contents[index])
                except:
                    return False
        else:
            return False

   
    def get_factoid(self, name):
        for i in self.factoids:
            if i.name.lower() == name.lower():
                return i
            
        return False
    
    class factoid:
        def __init__(self, name, contents):
            self.name = name
            self.contents = [contents]

import os, sys, xml.dom.minidom

def load_factoids(path):
    """Loads the users"""
    xmlDoc = xml.dom.minidom.parse(path)
    import factoids
    factoidManager = factoid_manager()
    for factoidElement in xmlDoc.getElementsByTagName("factoid"):
        name = getAttribute(factoidElement.attributes, "name")
        #Get the contents
        for contentElement in factoidElement.getElementsByTagName("content"):
            factoidManager.add_factoid(name, str(getAttribute(contentElement.attributes, "content")))
        
    return factoidManager

def save_factoids(factoid_manager, path):
    """Saves the users"""
    xmlDoc = xml.dom.minidom.parseString("<factoids></factoids>")
    
    for i in factoid_manager.factoids:
        factoidElement = xmlDoc.createElement("factoid")
        factoidElement.setAttribute("name", i.name)
        
        for content in i.contents:
            print content
            contentElement = xmlDoc.createElement("content")
            contentElement.setAttribute("content", content)

            factoidElement.appendChild(contentElement)
            
        xmlDoc.documentElement.appendChild(factoidElement)
    
    f = open(path, "w")
    f.write(xmlDoc.toprettyxml(indent="    "))
    return True

def getAttribute(attrlist, attrName):
    txt = ""
    #Loop through the attributes
    for i in range(0,attrlist.length):
        #If the attributes name == attrName
        if attrlist.item(i).nodeName == attrName:
            txt=attrlist.item(i).nodeValue
    #Then return the attributes value
    return txt
