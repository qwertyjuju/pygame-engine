import sys
import logging
import weakref
import importlib
import logging.handlers
from pathlib import Path
import pygame as pg
import managers
import gameentity
from version import *
DEPENDENCIES = {
    "src": "import",
    "logs": 0,
    "data": 0
}
current_dir = Path.cwd()
for key in DEPENDENCIES.keys():
    dependency_dir = Path.joinpath(current_dir, key)
    if DEPENDENCIES[key] == "import":
        try:
            importlib.import_module(key)
        except ModuleNotFoundError as e:
            DEPENDENCIES[key] = "ModuleNotFoundError - " + str(e)
        except ImportError as e:
            DEPENDENCIES[key] = "ImportError - " + str(e)
        else:
            sys.path.insert(0, str(DEPENDENCIES[key]))
    else:
        if dependency_dir.exists():
            DEPENDENCIES[key] = dependency_dir
        else:
            DEPENDENCIES[key] = 0

__version__ = str(VER)


class Engine:
    def __init__(self, configfilepath, logging_active=False):
        """
        On initialisation of the engine, several objects are created,
        """
        self.init_logger(logging_active)
        pg.init()
        gameentity.GameEntity.engine = self
        gameentity.GameEntity.set_subclasses()
        self.log("info", "Gamentities :", str(gameentity.GameEntity.get_subclasses()))
        self.events = None
        self.updatedict = {}
        self.updatelist = self.updatedict.values()
        self.datamanager = managers.DataManager(self)
        self.config = self.get_data(configfilepath)
        self.log("info", "Engine config :", str(self.config))
        for path in self['dataconfig']['_preload']:
            self.load_data(path)
        self.displaymanager = managers.DisplayManager(self)
        self.clock = pg.time.Clock()
        self.meanfps = 0
        self.count = 1
        self.log("info", "engine initialised successfully")

    def init_logger(self, logging_active):
        """
        creates logger object if parameter logging_active is true.
        The logger has 2 handlers: One handler for showing logs in terminal
        and one handler for saving logs in file.
        """
        self.logging = logging_active
        if self.logging:
            self.logger = logging.getLogger('Engine V' + __version__)
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
            sh = logging.StreamHandler()
            sh.setLevel(logging.WARNING)
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
            if DEPENDENCIES['logs']:
                fh = logging.handlers.RotatingFileHandler(filename="logs\\engine_logs_v" + __version__ + ".log",
                                                          maxBytes=1048576, backupCount=5, encoding="utf-8")
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)
        self.log("warning", "_____________________________ENGINE CREATION_____________________________ \n Engine version:", __version__)
        for dependency, value in DEPENDENCIES.items():
            if not value:
                self.log("warning", "dependency :", dependency, "- not found")
            if isinstance(value, str):
                if value.split(" - ")[0] in ["ImportError", "ModuleNotFoundError"]:
                    self.log("error", "dependency :", dependency, "-", value)

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
            if self.meanfps == 0:
                self.meanfps = self.fps
            self.meanfps = (self.meanfps+self.fps)/2
            self.displaymanager.set_caption(self.meanfps)

    def log(self, logtype, *texts):
        if self.logging:
            text = " ".join(texts)
            if logtype.lower() == "info":
                self.logger.info(text)
            elif logtype.lower() == "warning":
                self.logger.warning(text)
            elif logtype.lower() == "error":
                self.logger.error(text)
            else:
                self.logger.warning("message type incorrect. Message: " + text)
            
    def get_events(self):
        return self.events
    
    def get_data(self, dataname):
        return self.datamanager[dataname]
        
    def load_data(self, dataname, get=False):
        data = self.datamanager.load(dataname, get)
        if get:
            return data
        
    def create_scene(self, sceneid, sceneareas=None):
        return self.displaymanager.create_scene(sceneid, sceneareas)

    def get_scene(self, sceneid):
        return self.displaymanager[sceneid]
        
    def add_updatedentity(self, entity):
        self.updatedict[entity.entityID] = weakref.ref(entity)
        
    def del_updatedentity(self, entity):
        del self.updatedict[entity.entityID]

    def __getitem__(self, index):
        return self.config[index]

    def __contains__(self, item):
        if item in self.config:
            return True
        else:
            return False

    def quit(self):
        self.log("info", "fps mean : "+str(self.meanfps))
        self.log("warning", "_____________________________ ENGINE QUIT _____________________________ \n")
        logging.shutdown()
        pg.quit()
        sys.exit()
