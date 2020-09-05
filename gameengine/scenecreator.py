import pickle
from _managers import *
from _scene import *

readmode = False

elementlist1 =[(SceneElement,[(0,0),(300,300)]),(SceneElement,[(315,0),(300,300)]),(SceneElement,[(0,315),(300,300)]),(SceneElement,[(315,315),(300,300)]),]

scenesdict = {
    0:{'elemlist':elementlist1},
}



def createscenefile(scenedict):
    with open('scenes.scene','xb') as file:
        pickle.dump(scenedict, file)
        
def readscenefile():
    with open('scenes.scene','rb') as file:
        data = pickle.load(file)
        print(data)
        
if readmode:
    readscenefile()
else:
    createscenefile(scenesdict)

    