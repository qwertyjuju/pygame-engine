from engine.gameentity import GameEntity


def init():
    Map("data\\map\\map.json", "scene1")


class World(GameEntity):
    def init(self, datapath, sceneid):
        self.data = self.engine.get_data(datapath)


class Map(GameEntity):
    def init(self, datapath, sceneid):
        self.data = self.engine.get_data(datapath)
        self.scene = self.engine.get_scene(sceneid)
        #self.scene.create_scenearea("")

init()
