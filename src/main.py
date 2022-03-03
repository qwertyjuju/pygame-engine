from engine.gameentity import GameEntity
import numpy as np


class World(GameEntity):
    def init(self, datapath, sceneid):
        self.data = self.engine.get_data(datapath)
        self.scene = self.engine.get_scene(sceneid)
        self.scene.activate()


class Map(GameEntity):
    def init(self, datapath, scene, sceneid1):
        self.data = self.engine.get_data(datapath)
        self.area = scene.create_scenearea("Map", (0, 0), (1500, 1000))
        self.bg = self.area.create_surface("image", (0, 0), "data\\map\\gamemap.jpg")
        self.bg.convert()

    def update(self):
        self.bg.move(-1, -1)

class Player(GameEntity):
    def init(self):
        pass

World("data/map/world.world")
