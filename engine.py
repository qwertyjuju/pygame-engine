import sys, logging, weakref, statistics, importlib
import logging.handlers
from pathlib import Path
import pygame as pg
import managers
import gameentity

DEPENDENCIES={
    'src':"import",
    'logs':0,
    'data':0
}
current_dir = Path.cwd()
for key in DEPENDENCIES.keys():
    dependency_dir = Path.joinpath(current_dir, key)
    if dependency_dir.exists():
        DEPENDENCIES[key] = dependency_dir
        if DEPENDENCIES[key] == "import":
            try:
                importlib.import_module(key)
            except ImportError:
                DEPENDENCIES[key] = "ImportError"
            else:
                sys.path.insert(0, str(DEPENDENCIES[key]))
    else:
        DEPENDENCIES[key]=0

__version__ = "0.2"

class Engine:
    a: int = None
    fps: float = 0.0

    def __init__(self, configfilepath, logging_active=False):
        self.logging = logging_active
        if self.logging:
            self.set_logger()
        self.log("warning", "__________ENGINE CREATION__________ \n Engine version: "+__version__)
        for key, value in DEPENDENCIES.items():
            if not value:
                self.log("warning", "dependency : " + key + " - not found")
            if value == "ImportError":
                self.log("warning", "dependency : " + key + " - Import error. Module not imported")
        pg.init()
        gameentity.GameEntity.engine = self
        gameentity.GameEntity.set_subclasses()
        self.log("info", "Gamentities : " +str(gameentity.GameEntity.get_subclasses()))
        self.events = None
        self.updatedict = {}
        self.updatelist = self.updatedict.values()
        self.datamanager = managers.DataManager(self)
        self.config = self.load_data(configfilepath, get=True)
        self.log("info", "Engine config : " + str(self.config))
        for path in self['DataConfig']['_preload']:
            self.load_data(path)
        self.displaymanager = managers.DisplayManager(self)
        self.clock = pg.time.Clock()
        self.fpslist = []
        self.log("info", "engine initialised successfully")

    def set_logger(self):
        self.logger = logging.getLogger('Engine V' + __version__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)
        if DEPENDENCIES['logs']:
            fh = logging.handlers.RotatingFileHandler(filename="logs\engine_logs_v" + __version__ + ".log", maxBytes=1048576, backupCount=5, encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

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

    def log(self, type, message):
        if self.logging:
            if type.lower() == "warning":
                self.logger.warn(message)
            elif type.lower() == "info":
                self.logger.info(message)
            else:
                self.logger.warn("message type incorrect. Message: " + message)
            
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

    def __getitem__(self, index):
        return self.config[index]

    @staticmethod
    def quit():
        logging.shutdown()
        pg.quit()
        sys.exit()


