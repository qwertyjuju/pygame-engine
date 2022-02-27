from engine.gameentity import GameEntity
import numpy as np

class Map(GameEntity):
    def init(self, datapath, sceneid, sceneid1):
        self.data = self.engine.get_data(datapath)
        self.scene = self.engine.get_scene(sceneid)
        self.scene1 = self.engine.get_scene(sceneid1)
        self.scene.activate()
        self.area = self.scene.create_scenearea("Map", (0, 0), (1500, 1000))
        self.bg = self.area.create_surface("image", (0, 0), "data\\map\\gamemap.jpg")
        self.bg.convert()

    def update(self):
        self.bg.move(-1, -1)


Map("data\\map\\map.json", "scene1", "scene2")
