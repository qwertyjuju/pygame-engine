# import os
# import inspect
import sys
import weakref
import logging
from pathlib import Path
import pygame as pg
import managers
import gameentity
import statistics
current_dir = Path.cwd()
src_dir = Path.joinpath(current_dir, 'src')
data_dir = Path.joinpath(current_dir, 'data')
if src_dir.exists():
    sys.path.insert(0, str(src_dir))
    import src
    """
    try:
        import src
    except ImportError:
        print('src package not imported')
    """
else:
    print('no src package found')

__version__ = "0.2"


class Engine:
    a: int = None
    fps: float = 0.0

    def __init__(self, configfilepath):
        pg.init()
        gameentity.GameEntity.engine = self
        self.events = None
        self.updatedict = {}
        self.updatelist = self.updatedict.values()
        self.datamanager = managers.DataManager(self)
        self.config = self.load_data(configfilepath, get=True)
        for path in self['DataConfig']['_preload']:
            self.load_data(path)
        if self['settings']['logging']:
            print("bite")
            logging.basicConfig(filename='engine_v'+__version__+'.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG, filemode='x')
        self.displaymanager = managers.DisplayManager(self)
        self.clock = pg.time.Clock()
        self.fpslist = []
        self.log("info", "################ engine initialised ################")

    def run(self):
        while True:
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.quit()
            for entity in self.updatelist:
                entity().update()
            self.displaymanager.update()        
            self.clock.tick()
            self.fps = self.clock.get_fps()
            if len(self.fpslist)<10000:
                self.fpslist.append(self.fps)
            else:
                print(statistics.mean(self.fpslist))
                self.quit()
            self.displaymanager.set_caption(self.fps)
            
    def get_events(self):
        return self.events
    
    def get_data(self, dataname):
        return self.datamanager[dataname]
        
    def load_data(self, dataname, get=False):
        data = self.datamanager.load(dataname, get)
        if get:
            return data
        
    def create_scene(self):
        pass
        
    def add_updatedentity(self, entity):
        self.updatedict[entity.ID] = weakref.ref(entity)
        
    def del_updatedentity(self, entity):
        del self.updatedict[entity.ID]

    def log(self, type, message):
        def info():
            logging.info(message)
        def warning():
            logging.warning(message)
        if type.lower() == "warning":
            warning()
        if type.lower() == "info":
            info()
        else:
            message = 'message type incorrect. Message: '+message
            warning()

    def __getitem__(self, index):
        return self.config[index]

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()


gameentity.GameEntity.get_subclasses()

