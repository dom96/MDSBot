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