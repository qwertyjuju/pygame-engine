__version__='0.0.2'
print(__file__)
import sys, statistics,os, inspect, pathlib
import pygame as pg
import managers
import gameobjects
currentdir = pathlib.Path.cwd()
srcdir = pathlib.Path.joinpath(currentdir,'src')
datadir = pathlib.Path.joinpath(currentdir,'data')
if srcdir.exists():
    sys.path.insert(0,str(srcdir))
    try:
        import src
    except ImportError:
        print('src package not imported')
else:
    print('no src package found')
import gameentity

"""
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
srcdir = currentdir+'\\src'
datadir = currentdir+ '\\data'
if os.path.exists(srcdir):
    sys.path.insert(0,srcdir)
    try:
        import src
    except ImportError:
        print('src package not imported')
else:
    print('no src package found')
"""   

class Engine:
    def __init__(self, configfilepath):
        gameentity.GameEntity.engine = self
        gameentity.GameEntity.get_subclasses()
        print(gameentity.GameEntity.entitydict)
        self.events = None
        self.init(configfilepath)
        

    def init(self,configfilepath):
        pg.init()
        self.datamanager = managers.DataManager(configfilepath)
        self.datamanager.init_config()
        #self.eventmanager= managers.EventManager()
        self.displaymanager = managers.DisplayManager()
        self.scenemanager = managers.SceneManager()
        self.clock = pg.time.Clock()
        self.fpslist = []

    def run(self):
        while True:
            gameentity.GameEntity.events = pg.event.get()
            for event in gameentity.GameEntity.events:
                if event.type == pg.QUIT:
                    self.quit()
            #self.eventmanager.run()
            self.scenemanager.run()
            self.displaymanager.run()        
            self.clock.tick()
            self.fps=self.clock.get_fps()
            """
            if len(self.fpslist)<10000:
                self.fpslist.append(self.fps)
            else:
                print(statistics.mean(self.fpslist))
                self.quit()
            """
            self.displaymanager.set_caption(self.fps)

    def quit(self):
        pg.quit()
        sys.exit()
            
