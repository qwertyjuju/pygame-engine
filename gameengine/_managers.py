import os
import pickle
import pygame as pg
from pygame.locals import *

import common
import _gameobject as gameobject
from _scene import *
try:
    from src import *
except ImportError:
    print('game package not found')

class Manager:
    """Mother class for all managers."""
    def __init__(self):
        self.identifier = self.__class__.__name__ 
        self.loaderdict = common.LOADERDICT
        self.datadict = common.DATADICT
        self.eventdic = common.EVENTDICT
        self.statedict = {
            'active': True,
            'initialized': False,
        }
    
    def run(self):
        if self.statedict['active']:
            if self.statedict['initialized']:
                self.update()
            else:
                self.call_initializer()
                if self.statedict['initialized']:
                    self.update()
                else:
                    pass
            
    
    def call_initializer(self):
        try:
            self.initialize
        except AttributeError:
            self.statedict['initialized'] = True
        else:
            self.initialize()
            
    def get_data(self):
        

class DataManager(Manager):
    """
    The Datamanager Manages the loading and unloading of the different data parts
    when a component is loaded, the manager will try to find some standard keywords.
    Those keywords will do different operations. for example all images are are found
    under 'img' keyword. It must be a list of surface strings. The datamanager will go
    through the list and create a surface with pg.image.fromstring() function.
    """
    def __init__(self):
        super().__init__()
    
    def update(self):
        if len(self.loaderdict['_loadlist'])>0:
            print(self.loaderdict['_loadlist'])
            for elementnb, element in enumerate(self.loaderdict['_loadlist']):
                self.load(**element)
            self.loaderdict['_loadlist'] = []
        if len(self.loaderdict['_unloadlist'])>0:
            print(self.loaderdict['_unloadlist'])
            for elementnb, element in enumerate(self.loaderdict['_unloadlist']):
                self.unload(element)
            self.loaderdict['_unloadlist']= []
        
    
    def load(self,file,name):
        with open(file,'rb') as file:
            data = pickle.load(file)
        try:
            data['_img']
        except KeyError:
            pass
        else:
            self.loadimg(data['_img']) 
        self.datadict[name] = data
        
    def loadimg(imglist):
        for imgnb, img in enumerate(imglist):
            imglist[imgnb] = pg.image.fromstring(img[0],img[1],'RGBA')
        
    def unload(self,element):
        del self.datadict[element]
    
    def __repr__(self):
        return repr(self.datadict)
    
class EventManager(Manager):
    """
    Event Manager
    """
    def __init__(self):
        super().__init__()

    def update(self):
        for event in pg.event.get():
            if event.type == QUIT:
                common.GAMERUNNING = False
                return
            
class DisplayManager(Manager):
    """
    Display Manager
    """
    def __init__(self):
        super().__init__()
        self.width = common.SCREENWIDTH
        self.height = common.SCREENHEIGHT
        self.size = self.width, self.height
        self.screen = pg.display.set_mode(self.size)
        
    def update(self):
        self.screen.fill((0,0,0))
        self.screen.blits(common.BLITLIST)
        pg.display.flip()
        
        
class SceneManager(Manager):
    """
    container for the scenes. changes scene when changescene() is called. 
    Each scene has an ID used for changing scenes. The first active scene is
    always the sceneID =0.
    The SceneManager uses the data loaded from the '.scene' file. The structure
    of the dictionary inside the scene file is:
    
    datadict['scenes']={
        sceneID: {
            'sceneparam' : elementlist,
        },
        ...,
    }
    
    the elementlist is a list of tuples. The first element of each tuple is 
    a SceneElement class and the second element is the parameters for this scene
    element:
    
    elementlist= [
        (SceneElement, SceneElement params),
        ...,
    ]
    
    To create a Scene file, you can use the 'scene_creator.py' in the 'gametools'
    folder.
    """

    def __init__(self):
        super().__init__()
        self.scenedict = {}
    
    def initialize(self):
        try:
            self.datadict['scenes']
        except KeyError:
            pass
        else:
            for sceneID, sceneparam in self.datadict['scenes'].items():
                sceneparam['ID'] = int(sceneID) 
                sceneparam['scenemanager'] = self
                self.scenedict[sceneID] = Scene(**sceneparam)
            self.loaderdict['_unloadlist'].append('scenes')
            self.nbscenes = len(self.scenedict)
            self.activesceneID = 0
            self.statedict['initialized'] = True
            
    def update(self):
        if self.scenedict[self.activesceneID].active == False:
            self.scenedict[self.activesceneID].initialize()
            updatedscene = self.scenedict[self.activesceneID].update()
        else:
            updatedscene = self.scenedict[self.activesceneID].update()
        common.BLITLIST = updatedscene
        
    def changescene(self, sceneID):
        self.scenedict[self.activesceneID].uninitialize
        self.activesceneID = sceneID
        
class GameObjectManager(Manager):
    '''
    Manager for GameObjects. Calls the update method of all the GameObjectGroup
    '''
    
    def __init__(self, sceneelement):
        super().__init__()
        self.sceneelement = sceneelement
        self.groupsdict = {
            'main'= gameobject.GameObjectGroup(),
        }
        self.groupslist = self.groupsdict.values()
        
    def creategroup(self, groupname):
        self.groupsdict[groupname] = gameobject.GameObjectGroup()
        
    def addobjtogroup(self):
        try:
            self.manager.groups[self.groupname]
        except KeyError:
            self.manager.creategroup(self.groupname)
        else:
            self.manager.groups[self.groupname].addobject(self)
    
    def initialize(self):
        for gobject in self.objectlist:
            gobject[0](goject[1])

        
"""
BIN:
class GameObjectManager(Manager):
    
    def __init__(self,objectlist):
        super().__init__()
        self.groups = {
            'main'= gameobject.GameObjectGroup(),
        }
        self.objectlist = objectlist
        self.initialize()
        
    def drawlist(self):
        for gameobject in self.list:
            surface.blit(gameobject.surface,gameobject.pos)
            
    def update(self):
        for gameobject in self.updatelist:
            gameobject.run()
    
    def initialize(self):
        for gobject in self.objectlist:
            self.updatelist.append(gobject())
        self.statedict['initialized'] = True
"""
