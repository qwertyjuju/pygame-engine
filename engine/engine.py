import importlib
import logging
import logging.handlers
import sys
import weakref
from pathlib import Path

import pygame as pg

import engine.gameentity as gameentity
import engine.managers as managers
from engine.version import *

DEPENDENCIES = {
    "src": "import",
    "logs": 0,
    "data": 0
}

__version__ = str(VER)


def init_logger():
    """
    creates logger object if parameter logging_active is true.
    The logger has 2 handlers: One handler for showing logs in terminal
    and one handler for saving logs in file.
    """
    logger = logging.getLogger('Engine V' + __version__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    fh = logging.handlers.RotatingFileHandler(filename="logs\\engine_logs_v" + __version__ + ".log",
                                              maxBytes=1048576, backupCount=5, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def log(logtype, *texts):
    text = " ".join(texts)
    if logtype.lower() == "info":
        LOGGER.info(text)
    elif logtype.lower() == "warning":
        LOGGER.warning(text)
    elif logtype.lower() == "error":
        LOGGER.error(text)
    else:
        LOGGER.warning("message type incorrect. Message: " + text)


class Engine:
    def __init__(self, configfilepath, enable_logging=0):
        # On initialisation of the engine, several objects are created,
        self.logging = enable_logging
        self.log("warning",
                 "_____________________________ENGINE CREATION_____________________________ \n Engine version:",
                 __version__)
        pg.init()
        gameentity.GameEntity.set_engine(self)
        self.events = None
        self.updatedict = {}
        self.updatelist = self.updatedict.values()
        self._datamanager = managers.DataManager(self)
        self.config = self.get_data(configfilepath)
        self.log("info", "Engine config :", str(self.config))
        for path in self['dataconfig']['_preload']:
            self.load_data(path)
        self._displaymanager = managers.DisplayManager(self)
        self.clock = pg.time.Clock()
        self.meanfps = 0
        self.init_dependencies()
        self.log("info", "Gamentities :", str(gameentity.GameEntity.get_subclasses()))
        self.log("info", "engine initialised successfully")

    def run(self):
        while True:
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.quit()
            for entity in self.updatelist:
                entity().update()
            self._displaymanager.update()
            self.clock.tick()
            self.fps = self.clock.get_fps()
            if self.meanfps == 0:
                self.meanfps = self.fps
            self.meanfps = (self.meanfps+self.fps)/2
            self._displaymanager.set_caption(self.fps)

    def log(self, logtype, *texts):
        if self.logging:
            log(logtype, *texts)
        
    def load_data(self, dataname, get=False):
        data = self._datamanager.load(dataname, get)
        if get:
            return data
        
    def create_scene(self, sceneid, sceneareas=None):
        return self._displaymanager.create_scene(sceneid, sceneareas)

    def get_events(self):
        return self.events

    def get_data(self, datapath):
        return self._datamanager[datapath]

    def get_scene(self, sceneid):
        return self._displaymanager[sceneid]
        
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
        self.log("info", "quitting")
        self.log("info", "fps mean : "+str(self.meanfps))
        self.log("warning", "_____________________________ ENGINE QUIT _____________________________ \n")
        self.logging = 0
        logging.shutdown()
        pg.quit()
        sys.exit()

    @staticmethod
    def init_dependencies():
        current_dir = Path.cwd()
        for key in DEPENDENCIES.keys():
            dependency_dir = Path.joinpath(current_dir, key)
            if DEPENDENCIES[key] == "import":
                try:
                    importlib.import_module(key)
                except ModuleNotFoundError as e:
                    DEPENDENCIES[key] = "ModuleNotFoundError - " + str(e)
                    log("error", "dependency :", key, "-", DEPENDENCIES[key])
                except ImportError as e:
                    DEPENDENCIES[key] = "ImportError - " + str(e)
                    log("error", "dependency :", key, "-", DEPENDENCIES[key])
                else:
                    sys.path.insert(0, str(DEPENDENCIES[key]))
                    log("info", "dependency :", key, "-", "imported successfully")
            else:
                if dependency_dir.exists():
                    DEPENDENCIES[key] = dependency_dir
                else:
                    log("warning", "dependency :", key, "- not found")


LOGGER = init_logger()
