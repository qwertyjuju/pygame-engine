import pygame as pg
import _managers as manager

   
class GameObject:
    def __init__(self, manager, group = 'main', priority = 0):
        self.name = self.__class__.__name__
        self.manager = manager
        self.priority = priority
        self.groupname = group
        self.statedict = {
            'active': True,
            'initialized': False,
            'draw': False
        }
        self.pos = pos
        self.addtogroup()

    
    def run(self):
        if self.statedict['initialized']:
            if self.statedict['active']:
                pass
        else:
            self.call_initializer()
        self.update()
            
    def call_initializer(self):
        try:
            self.initialize
        except AttributeError:
            self.statedict['initialized'] = True
        else:
            self.initialize()
            
    
            
    def get_surface(self):
        return self.surf, self.pos

class GameObjectGroup:
    """
    Container for Gameobjects
    """
    
    def __init__(self):
        self.golist =[]

    
    def addobject(self,gobject):
        self.golist.append(gobject)
        self.golist.sort(key = lambda x: x.priority)
        
    
    