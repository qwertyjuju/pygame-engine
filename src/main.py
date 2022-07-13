import numpy as np
from pathlib import Path
from engine.gameentity import GameEntity

class Ui:
    pass

class World(GameEntity):
    def init(self, datapath, sceneid):
        parent = self.get_datapath(datapath).parent
        self.data = self.engine.get_data(datapath)
        self.maps = []
        for map in self.data["maps"]:
            self.maps.append(Map(str(parent.joinpath(map["fileName"]))))
        self.scene = self.engine.get_scene(sceneid)
        self.area = self.scene.create_scenearea("Map", (0, 0), (1800, 950))
        self.maps[0].load(self.area)
        self.scene.activate()


class Map(GameEntity):
    def init(self, datapath):
        self.data = self.engine.get_data(datapath)

    def load(self, area):
        self.bg = area.create_surface("image", (0, 0), "data|map|gamemap.jpg")
        self.engine.add_event_listener("keyboard", "d", self.bg.move, (-5,0), 10)
        self.engine.add_event_listener("keyboard", "q", self.bg.move, (5, 0), 10)
        self.engine.add_event_listener("keyboard", "z", self.bg.move, (0, 5), 10)
        self.engine.add_event_listener("keyboard", "s", self.bg.move, (0, -5), 10)
        self.bg.convert()


class Player(GameEntity):
    def init(self):
        pass

World("data|map|world.world","scene1")