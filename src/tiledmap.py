import numpy as np
import pygame as pg
from pygame.locals import *
from pygame.math import Vector2 as Vec
from gameentity import GameEntity
from gameobjects import *
import math
from pathlib import Path

class TiledMap(SceneObject):
    def init(self, filename, sceneareaid, sceneareasize, sceneareapos):
        self.data= self.get_data(filename)
        self.path = self.data['_dir']
        self.camera = self.scene.create_scenearea(sceneareaid,sceneareasize, sceneareapos)
        self.camerapos = Vec(0,0)
        self.height = self.data['height']
        self.width = self.data['width']
        self.tilewidth = self.data['tilewidth']
        self.tileheight = self.data['tileheight']
        self.chunkwidth = self.data['layers'][0]['chunks'][0]['height']
        self.chunkheight =self.data['layers'][0]['chunks'][0]['width']
        self.size = [self.width,self.height]
        self.chunkpixelsize= [self.chunkwidth*self.tilewidth,self.chunkheight*self.tileheight]
        self.pixelsize = [self.width*self.tilewidth,self.height*self.tileheight]
        self.tiles = {}
        self.layers = []
        self.chunks = np.empty(((math.ceil(self.width/self.chunkwidth),math.ceil(self.height/self.chunkheight))),dtype =object)
        self.init_tilesets()
        self.init_layers()
        print(self.chunks.shape)
        self.buffer =ChunkBuffer(self,(3,3),(7,2))
        #self.player= pg.image.load('player.png').convert_alpha()
    
    def init_tilesets(self):
        for tilesetparams in self.data['tilesets']:
            Tileset(self,**tilesetparams).load()
    
    def init_layers(self):
        for layer in self.data['layers']:
            if layer['type'] == 'tilelayer':
                TileLayer(self,layer)

    def add_tile(self, tile):
        self.tiles[tile.gid] = tile
    
    def add_layer(self,layer):
        self.layers.append(layer)
        
    def add_chunk(self, chunk):
        x = int(chunk.x/chunk.width)
        y = int(chunk.y/chunk.height)
        if self.chunks[x,y] is None:
            self.chunks[x,y] = []
        self.chunks[x,y].append(chunk)

    def renderchunk(self,x,y,pos):
        print(x,y,pos)
        surface = GameSurface(self.camera,(self.tilewidth*self.chunkwidth,self.tileheight*self.chunkheight),pos,SRCALPHA)
        for chunk in self.chunks[x,y]:
            surface.blits(chunk.renderlist)
        return surface
                
    def update(self):
        for event in self.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    self.buffer.move(-100,0)
                if event.key == pg.K_q:
                    self.buffer.move(100,0)
                if event.key == pg.K_s:
                    self.buffer.move(0,-100)
                if event.key == pg.K_z:
                    self.buffer.move(0,100)
                    
class TiledObject(GameEntity):
    def __init__(self,tiledmap, *args, **kwargs):
        super().__init__()
        self.tiledmap = tiledmap
        try:
            self.init
        except AttributeError:
            pass
        else:
            self.init(*args,**kwargs)
        
            
class Tileset(TiledObject):
    def init(self, firstgid, source):
        self.firstgid = firstgid
        self.source = source
        self.path = self.tiledmap.path / Path(self.source)

    def load(self):
        self.engine.datamanager.createfile(self.path, load=True)
        self.data = self.get_data(self.source)
        self.imagepath = self.tiledmap.path / Path(self.data['image'])
        self.engine.datamanager.createfile(self.imagepath, load=True)
        self.image = self.get_data(self.data['image'])['img']
        self.create_tiles()
        
    def create_tiles(self):
        i = self.firstgid
        tilesize = self.data["tileheight"],self.data["tilewidth"]
        for y in range(0,self.data["imageheight"],self.data["tileheight"]):
            for x in range(0,self.data["imagewidth"],self.data["tilewidth"]):
                Tile(self.tiledmap,i, x, y, tilesize).load(self.image)
                i+=1
                
class Tile(TiledObject):
    def init(self, gid, x, y, tilesize):
        self.gid = gid
        self.x=x
        self.y=y
        self.size = tilesize
        self.tiledmap.add_tile(self)
        
    def load(self, tilesetimage):
        self.surf = tilesetimage.get_tile(self.x,self.y,self.size)
        
    def get_surface(self):
        return self.surf
        
class TileLayer(TiledObject):
    def init(self,layerdata):
        self.type =layerdata['type']
        self.tiledmap.add_layer(self)
        for chunk in layerdata['chunks']:
            Chunk(self.tiledmap,chunk)
        
class Chunk(TiledObject):
    def init(self, chunkdict):
        self.height = chunkdict['height']
        self.width = chunkdict['width']
        self.x = chunkdict['x']
        self.y = chunkdict['y']
        self.data = np.array(chunkdict['data']).reshape(-1,self.width)
        self.create_renderlist()
        self.tiledmap.add_chunk(self)

    def create_renderlist(self):
        self.renderlist = []
        for rownb, row in enumerate(self.data):
            for cellnb, tile in enumerate(row):
                if tile ==0:
                    pass
                else:
                    self.renderlist.append((self.tiledmap.tiles[tile].get_surface(),(cellnb*self.tiledmap.tilewidth,rownb*self.tiledmap.tileheight)))
                    
class ChunkBuffer(TiledObject):
    def init(self,shape, firstpos = None):
        self.shape = shape
        self.surfaces = np.empty(shape,dtype =object)
        if firstpos is not None:
            self.renderchunks(*firstpos)
            
    def renderchunks(self,x,y):
        if x<0:
            x=0
        if y<0:
            y=0
        if x>=self.tiledmap.chunks.shape[1]:
            x=self.tiledmap.chunks.shape[1]-2
        if y>=self.tiledmap.chunks.shape[0]:
            y=self.tiledmap.chunks.shape[0]-2
        dx=x
        dy=y    
        for rownb,row in enumerate(self.surfaces):
            for cellnb,cell in enumerate(row):
                pos= cellnb*self.tiledmap.chunkpixelsize[1],rownb*self.tiledmap.chunkpixelsize[0]
                #pos= rownb*self.tiledmap.chunkpixelsize[0],cellnb*self.tiledmap.chunkpixelsize[1]
                self.surfaces[rownb,cellnb]= self.tiledmap.renderchunk(dx,dy,pos)
                dx+=1
            dy+=1
            dx=x
                
    def move(self,dx,dy):
        for rownb,row in enumerate(self.surfaces):
            for cellnb,cell in enumerate(row):
                self.surfaces[rownb,cellnb].move(dx,dy)
            
            
                    
"""                  
class TiledSurfaceBuffer(TiledObject):
    def init(self, buffershape):
        
                    
class TiledSurface(TiledObject):
    def init(self)
"""  