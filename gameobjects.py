import pygame as pg
from pygame.math import Vector2 as Vec
from gameentity import GameEntity


class Scene(GameEntity):
    
    def init(self, display, ID, *args):
        self.display = display
        self.ID = ID

    def get_subsurface(self, area):
        return self.display.screen.subsurface(area)


class SceneArea(GameEntity):

    def init(self, scene, pos, size):
        self.scene = scene
        self.render_list = []
        self.set_area(pos, size)
        self.scene.get_subsurface(self.area)

    def set_area(self, pos, size):
        self.pos = pos
        self.size = size
        self.area = pos, size

    def create_gamesurface(self, pos, type="Empty", *args, **kwargs):
        if type == "Empty":
            EmptyGameSurface(self, pos, *args, **kwargs)
        if type == "Image":
            ImageGameSurface(self, pos, *args, **kwargs)
        
    def add_gamesurface(self, gamesurface):
        self.render_list.append([gamesurface.surface, gamesurface.pos])
        
    def update(self):
        self.render()
        
    def render(self):
        self.surface.blits(self.render_list)
        
    def clear(self):
        self.render_list.clear()

        
class SceneAreaObject(GameEntity):

    def __init__(self, scenearea, pos):
        self.scenearea = scenearea
        self.pos = Vec(pos)
        super.__init__()
        self.scenearea.add_Gamesurface(self)

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
        self.set_size(self.surface)
