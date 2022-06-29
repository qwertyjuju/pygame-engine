import numpy as np
from pathlib import Path
from engine.gameentity import GameEntity



class World(GameEntity):
    def init(self, datapath, sceneid):
        parent = Path(datapath).parent
        self.data = self.engine.get_data(datapath)
        self.maps = []
        for map in self.data["maps"]:
            self.maps.append(Map(parent.joinpath(map["fileName"])))
        self.scene = self.engine.get_scene(sceneid)
        self.maps[0].load(self.scene)
        self.scene.activate()


class Map(GameEntity):
    def init(self, datapath):
        self.set_update(0)
        self.data = self.engine.get_data(datapath)

    def load(self, scene):
        self.set_update(1)
        self.area = scene.create_scenearea("Map", (0, 0), (1500, 1000))
        self.bg = self.area.create_surface("image", (0, 0), "data\\map\\gamemap.jpg")
        self.bg.convert()

    def update(self):
        self.bg.move(-1, -1)


class Player(GameEntity):
    def init(self):
        pass

World("data/map/world.world","scene1")
