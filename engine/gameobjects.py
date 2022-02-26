import pygame as pg
from pygame.math import Vector2 as Vec

from engine.gameentity import GameEntity


class Scene(GameEntity):
    _register = 0

    def init(self, display, sceneid, sceneareas=None):
        self.display = display
        self.id = sceneid
        self._active = 0
        self.sceneareas = {}
        if sceneareas:
            for scenearea in sceneareas:
                self.create_scenearea(**scenearea)
        self.engine.log("info", "Scene created successfully. SceneID:", self.id)
        self.display.add_scene(self)

    def activate(self):
        for area in self.sceneareas.values():
            area.load()
        self._active = 1
        self.display.set_active_scene(self)

    def deactivate(self):
        for area in self.sceneareas.values():
            area.unload()
        self._active = 0

    def create_scenearea(self, sceneareid, pos, size):
        if sceneareid not in self.sceneareas:
            return SceneArea(self, sceneareid, pos, size)
        else:
            self.engine.log("error", "SceneArea not created, sceneAreaID already exists. SceneAreaID:", sceneareid)

    def add_scenearea(self, scenearea):
        self.sceneareas[scenearea.id] = scenearea
        if self._active:
            scenearea.load()

    def get_subsurface(self, area):
        return self.display.screen.subsurface(area)

    def get_areas(self):
        return self.sceneareas

    def __getitem__(self, item):
        return self.sceneareas[item]


class SceneArea(GameEntity):
    _register = 0

    def init(self, scene, sceneareaid, pos, size):
        self.scene = scene
        self.id = sceneareaid
        self._active = 0
        self.pos = pos
        self.size = size
        self.__set_area()
        self.objects = {}
        self.render_dict = {}
        self.render_list = []
        self.engine.log("info", "SceneArea created successfully. SceneAreaID:", self.id)
        self.scene.add_scenearea(self)

    def __set_area(self):
        self.area = self.pos, self.size
        if self._active:
            self.load()

    def set_pos(self, pos):
        self.pos = pos
        self.__set_area()

    def set_size(self, size):
        self.size = size
        self.__set_area()

    def create_surface(self, type, pos, *args, **kwargs):
        if type.lower() == "empty":
            return EmptyGameSurface(self, pos, *args, **kwargs)
        if type.lower() == "image":
            return ImageGameSurface(self, pos, *args, **kwargs)

    def add_surface(self, scenearea_object):
        self.objects[scenearea_object.entityID] = scenearea_object
        self.render_list.append([scenearea_object.surface, scenearea_object.pos])
        
    def update_surface(self, scenearea_object):
        self.render_list.append([scenearea_object.surface, scenearea_object.pos])

    def move_all(self, dx, dy):
        for object in self.objects.values():
            object.move(dx, dy)

    def load(self):
        self._active = 1
        self.surface = self.scene.get_subsurface(self.area)

    def unload(self):
        self._active = 0
        self.surface.fill((0, 0, 0), self.area)
        del self.surface
        
    def render(self):
        self.surface.fill((0,0,0),self.area)
        self.surface.blits(self.render_list)
        
    def clear(self):
        self.render_list.clear()

        
class SceneAreaObject(GameEntity):
    _register = 0

    def __init__(self, scenearea, pos, *args, **kwargs):
        self.scenearea = scenearea
        self.pos = Vec(pos)
        self.surface = None
        super().__init__(*args, **kwargs)
        self.scenearea.add_surface(self)

    def convert(self):
        self.surface = self.surface.convert()

    def set_size(self, size):
        self.size = size

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    @classmethod
    def init_class(cls):
        cls.set_subclasses()


class EmptyGameSurface(SceneAreaObject):
    _register = 0

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
    _register = 0

    def init(self, imagename):
        self.surface = self.engine.get_data(imagename).get_surface()
        self.set_size(self.surface.get_size())
