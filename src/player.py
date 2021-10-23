from gameobjects import SceneObject
class Player(SceneObject):
    def init(self, filename, sceneareaid):
        self.data= self.get_data(filename)
        self.camera= self.scene.get_scenearea(sceneareaid)
        