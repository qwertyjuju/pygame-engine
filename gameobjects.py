import pygame as pg
from pygame.math import Vector2 as Vec
from gameentity import GameEntity


class Scene(GameEntity):
    
    def init(self, scenemanager):
        self.manager = scenemanager


class SceneArea(GameEntity):

    def init(self, scene, size, pos, clear=True):
        self.scene = scene
        self.pos = pos
        self.size = size
        self.area = pos, size
        self.render_list = []
        
    def create(self):
        pass
        
    def _add_gamesurface(self, gamesurface):
        print((gamesurface.surface, gamesurface.pos))
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
        super().__init__()

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy


class GameSurface(SceneAreaObject):

    def init(self, size, pos, flag=None, convertalpha=False):
        self.size = size
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
        self.scenearea.add_Gamesurface(self)
        
    def blit(self, surf, pos):
        self.surface.blit(surf, pos)

    def blits(self, blit_list):
        self.surface.blits(blit_list)
