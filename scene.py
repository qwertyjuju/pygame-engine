from gameentity import GameEntity
from gameobjects import SceneArea

class Scene(GameEntity):
    idlist = []
    def __new__(cls,*args, **kwargs):
        if type(kwargs['ID']) is not int:
            print(kwargs)
            print('Scene not created, ID is not int')
            return
        if kwargs['ID'] in Scene.idlist:
            print('Scene not created, ID already exists')
            return
        return super().__new__(cls)
    
    def __init__(self, ID, manager, objects):
        super().__init__()
        self.manager = manager
        self.ID = ID
        Scene.idlist.append(self.ID)
        self.objects = objects
        self.gameobjects = []
        self.sceneareasdict = {}
        self.sceneareaslist = self.sceneareasdict.values()
        self.manager.add_scene(self)
        
    def init(self):
        for sceneobject in self.objects:
            print(sceneobject)
            GameEntity.entitydict[sceneobject['objectname']](self,sceneobject['ID'],*sceneobject['paramlist'])

            
    def create_scenearea(self,ID,size,pos):
        return SceneArea(self,ID,size,pos)
        
    def add_scenearea(self, scenearea):
        print(scenearea.ID)
        self.sceneareasdict[scenearea.ID]= scenearea

    def add_gameobject(self,gameobject):
        self.gameobjects.append(gameobject)
        
    def get_scenearea(self, sceneareaid):
        return self.sceneareasdict[sceneareaid]
        
    def clear(self):
        self.sceneareas.clear()
            
    def update(self):
        for gameentity in self.gameobjects:
            gameentity.run()
        for scenearea in self.sceneareaslist:
            scenearea.run()

"""
class SceneArea(GameEntity):
    def __init__(self, scene, size, pos):
        super().__init__()
        self.scene = scene
        self.pos = pos
        self.size =size
        self.area = pos, size
        self.renderlist = []
        self.scene.add_scenearea(self)
        
    def addto_renderlist(self, surface, pos):
        self.engine.displaymanager.blit((surface,pos,self.area))
        
    def update(self):
        pass
        
    def render(self):
        self.engine.displaymanager.blits(self.renderlist)
        
    def clear(self):
        self.renderlist.clear()
"""