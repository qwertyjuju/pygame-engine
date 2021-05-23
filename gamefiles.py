import json, pickle, pathlib
import pygame as pg
from pygame.locals import *

class GameFile:
        
    def __init__(self, manager, path, customname = None):
        print(path)
        self.path = pathlib.Path(path)
        self.dir= self.path.parent
        self.type = self.path.suffix
        self.manager = manager
        if customname is None:
            self.name= self.path.name
        else:
            self.name = customname
        self.manager.addfile(self)
            
    def load(self):
        data = {}
        if self.type == '.json':
            with open(self.path, 'r') as file:
                data.update(json.load(file) )
        if self.type == '.png':
            data.update({
                'img':GameImage(self.path)
            })
        data['_dir'] = str(self.dir)
        self.manager.add_data(self, data)


    
class Spritesheet:
    pass