import sys, os, inspect
import pygame as pg
from pygame.math import Vector2 as Vec
from gameentity import GameEntity


class SceneObject(GameEntity):
    gameobjectidlist = []
    scenearealist =[]
    
    def __new__(cls,*args,**kwargs):
        if type(args[1]) is not int:
            print('SceneObject not created, ID is not int')
            return
        else:
            if issubclass(cls, SceneArea):
                if args[1] in SceneObject.scenearealist:
                    print('SceneArea not created, ID already exists')
                    return
            elif args[1] in SceneObject.gameobjectidlist:
                print('SceneObject not created, ID already exists')
                return
        return super().__new__(cls)
    
    def __init__(self, scene,ID,*args, **kwargs):
        super().__init__()
        self.scene = scene
        self.ID = ID
        if isinstance(self,SceneArea):
            self.scene.add_scenearea(self)
        else:
            self.scene.add_gameobject(self)
        try:
            self.init
        except AttributeError:
            pass
        else:
            self.init(*args,**kwargs)

class SceneArea(SceneObject):
    def init(self,size, pos, clear = True):
        self.pos = pos
        self.size =size
        self.area = pos, size
        self.surface = self.engine.displaymanager.createsubsurface(self.area)
        self.renderlist =[]
        
    def add_Gamesurface(self, gamesurface):
        print((gamesurface.surface,gamesurface.pos))
        self.renderlist.append([gamesurface.surface,gamesurface.pos]) 
        
    def update(self):
        self.render()
        
    def render(self):
        self.surface.blits(self.renderlist)
        
    def clear(self):
        self.renderlist.clear()

        
class SceneAreaObject(GameEntity):
    def __init__(self, scenearea,*args,**kwargs):
        super().__init__()
        self.scenearea = scenearea
        try:
            self.init
        except AttributeError:
            pass
        else:
            self.init(*args,**kwargs)
            
class GameSurface(SceneAreaObject):
    def init(self,size, pos, flag= None, convertalpha = False):
        self.size = size
        self.pos = Vec(pos)
        self.blitlist = []
        if convertalpha:
            if flag is None:
                self.surface = pg.Surface(self.size).convert_alpha()
            else:
                self.surface = pg.Surface(self.size,flag).convert_alpha()
        else:
            if flag is None:
                self.surface = pg.Surface(self.size).convert()
            else:
                self.surface = pg.Surface(self.size,flag).convert()
        self.scenearea.add_Gamesurface(self)

    def blits(self,blitlist):
        self.surface.blits(blitlist)
        
    def move(self,dx,dy):
        self.pos[0]+=dx
        self.pos[1]+=dy