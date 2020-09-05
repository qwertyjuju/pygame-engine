import pygame as pg
import _managers as manager

class Scene:
    """
    class for scene. Each scene has an ID and a list of SceneElements.
    On creation of the scene, the SceneElements are not initialized. Once
    the scene Manager activates a scene, it calls the initialize function
    wich will create all the SceneElements of the Scene.
    """
    def __init__(self,scenemanager,ID, elemlist):
        self.manager = scenemanager
        self.active = False
        self.ID = ID
        self.elemlist = elemlist
    
    def initialize(self):
        self.active = True
        self.updatelist = []
        for elemnb,element in enumerate(self.elemlist):
            element[1].insert(0,self)
            self.updatelist.append(element[0](*element[1]))
            
    def update(self):
        self.blitlist = []
        for element in self.updatelist:
            element.run()
        return self.blitlist
    
    def uninitialize(self):
        self.active = False
        del self.updatelist
        
    def addelement(self):
        pass
    
    def removeelement(self):
        pass

class SceneElement:
    """
    A Scene Element is a surface where gameobjects are blit on. This class
    can be used
    """
    def __init__(self, scene, pos, size, gameobjectlist = []):
        self.identifier = self.__class__.__name__
        self.loaderdict = common.LOADERDICT
        self.datadict = common.DATADICT
        self.eventdic = common.EVENTDICT
        self.statedict = {
            'active': True,
            'initialized': False,
        }
        self.scene = scene
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.surface = pg.Surface(self.size, pg.SRCALPHA)
        self.gameobjectlist = gameobjectlist
        self.manager = manager.GameObjectManager(self)
        

    def draw(self):
        self.surface.fill((0,0,0))
        self.surface.blits([])
    
    def run(self):
        if self.statedict['initialized']:
            if self.statedict['active']:
                try:
                    self.update
                except AttributeError:
                    pass
                else:
                    self.update()
                self.manager.run()
                self.draw()
                return (self.surface, self.pos)
        else:
            self.call_initializer()
        
        
    def call_initializer(self):
        try:
            self.initialize
        except AttributeError:
            self.statedict['initialized']= True
        else:
            self.initialize()
            
    def get_data(self):
        try:
            self.datadict[self.identifier]
        except KeyError:
            return 1
        else:
            self.data = self.datadict[self.identifier]
            return self.data