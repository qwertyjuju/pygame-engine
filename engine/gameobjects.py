import pygame as pg
from pygame.math import Vector2 as Vec

from engine.gameentity import GameEntity


class Scene(GameEntity):
    
    def init(self, display, sceneid, sceneareas=None):
        self.display = display
        self.id = sceneid
        self.sceneareas = {}
        if sceneareas:
            for scenearea in sceneareas:
                self.create_scenearea(**scenearea)
        self.engine.log("info", "Scene created successfully. SceneID:", self.id)
        self.display.add_scene(self)

    def create_scenearea(self, sceneareid, pos, size):
        if sceneareid not in self.sceneareas:
            return SceneArea(self, sceneareid, pos, size)
        else:
            self.engine.log("error", "SceneArea not created, sceneAreaID already exists. SceneAreaID:", sceneareid)

    def add_scenearea(self, scenearea):
        self.sceneareas[scenearea.id] = scenearea

    def get_subsurface(self, area):
        return self.display.screen.subsurface(area)

    def __getitem__(self, item):
        return self.sceneareas[item]


class SceneArea(GameEntity):

    def init(self, scene, sceneareaid, pos, size):
        self.scene = scene
        self.id = sceneareaid
        self.render_list = []
        self.set_area(pos, size)
        self.objects = {}
        self.surface = self.scene.get_subsurface(self.area)
        self.engine.log("info", "SceneArea created successfully. SceneAreaID:", self.id)
        self.scene.add_scenearea(self)

    def set_area(self, pos, size):
        self.pos = pos
        self.size = size
        self.area = pos, size

    def create_object(self, type, pos, *args, **kwargs):
        if type.lower() == "empty":
            return EmptyGameSurface(self, pos, *args, **kwargs)
        if type.lower() == "image":
            return ImageGameSurface(self, pos, *args, **kwargs)

    def add_object(self, scenearea_object):
        self.objects[scenearea_object.entityID] = scenearea_object
        self.addto_renderlist(scenearea_object)
        
    def addto_renderlist(self, scenearea_object):
        self.render_list.append([scenearea_object.surface, scenearea_object.pos])

    def move_all(self):
        pass
        
    def update(self):
        self.render()
        
    def render(self):
        self.surface.blits(self.render_list)
        
    def clear(self):
        self.render_list.clear()

        
class SceneAreaObject(GameEntity):

    def __init__(self, scenearea, pos, *args, **kwargs):
        self.scenearea = scenearea
        self.pos = Vec(pos)
        self.surface=None
        super().__init__(*args, **kwargs)
        self.scenearea.add_object(self)

    def convert(self):
        self.surface.convert()

    def set_size(self, size):
        self.size=size

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy


class EmptyGameSurface(SceneAreaObject):

    def init(self, size, flag=None, convertalpha=False):
        self.set_size(size)
        self.blit_list = []
        if convertalpha:
            if flag is None:
                self.surface = pg.Surface(self.size).convert_alpha()
            else:
                self.surface = pg.Surface(self.size, flag).convert_alpha()
        else:
            if flag is None:
                self.surface = pg.Surface(self.size).convert()
            else:
                self.surface = pg.Surface(self.size, flag).convert()
        
    def blit(self, surf, pos):
        self.surface.blit(surf, pos)

    def blits(self, blit_list):
        self.surface.blits(blit_list)


class ImageGameSurface(SceneAreaObject):
    def init(self, imagename):
        self.surface = self.engine.get_data(imagename).get_surface()
        self.set_size(self.surface.get_size())
