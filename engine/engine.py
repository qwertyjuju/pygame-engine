import importlib
import logging
import logging.handlers
import sys
import weakref
import platform
from pathlib import Path

import pygame as pg

import engine.gameentity as gameentity
import engine.managers as managers
from engine.version import *



__version__ = str(VER)


class Engine:
    """
    main class for the engine
    """
    _DEPENDENCIES = {
        "import": ["src"],
        "set_path": ["data"]
    }

    def __init__(self):
        self.logging = 0
        self.updatedict = {}
        self.updatelist = self.updatedict.values()
        gameentity.GameEntity.e_set_engine(self)
        managers.Manager.e_set_engine(self)
        pg.init()

    def _init_logger(self, logspath=Path(f"logs{__version__}.log")):
        """
        creates logger object if parameter logging_active is true.
        The logger has 2 handlers: One handler for showing logs in terminal
        and one handler for saving logs in file.
        :param logspath:
        :return:
        """
        self._logger = logging.getLogger('Engine V' + __version__)
        self._logger.setLevel(logging.DEBUG)
        self.computer_info ={
            "os": platform.system(),
            "release": platform.release(),
            "python_ver": platform.python_version(),
            "processor": platform.processor()
        }
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        self._logger.addHandler(sh)

        fh = logging.handlers.RotatingFileHandler(filename=logspath,
                                                  maxBytes=10048576, backupCount=5, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self._logger.addHandler(fh)

    def run(self, configfilepath=None):
        """
        The run function is to be called at startup
        :param configfilepath:
        :return:
        """
        self.log("info",
                 f"_____________________________GAME START_____________________________ \n Engine version: {__version__} \n",
                 f"computer information: {self.computer_info}")
        self._datamanager = managers.DataManager()
        for path in self._DEPENDENCIES["set_path"]:
            self._datamanager.set_path(path)
        if configfilepath:
            self.config = self._datamanager[configfilepath]
            self.log("info", "Engine config :", str(self.config))
            try:
                for path in self.config['dataconfig']['preload']:
                    self.get_data(path)
            except KeyError:
                pass
        else:
            self.config= {
                "screensize":None
            }
        self._eventmanager = managers.EventManager()
        self._displaymanager = managers.DisplayManager(self.config["screensize"])
        for path in self._DEPENDENCIES["import"]:
            try:
                importlib.import_module(path)
            except Exception as e:
                self.log("error", "module :", path, " not imported:", str(e))
        self.log("info", "Gamentities :", str(gameentity.GameEntity.get_subclasses()))
        self.log("info", "engine initialised successfully")
        while True:
            self._eventmanager.update()
            for entity in self.updatelist:
                entity().update()
            self._displaymanager.update()

    def set_logger(self, logspath=None):
        """
        inits the logger
        :param logspath: log path. By default it will be in the current working directory
        :return:
        """
        self.logging = 1
        if logspath:
            logspath = Path(logspath)
            if logspath.exists():
                self._init_logger(logspath)
            else:
                self._init_logger()
        else:
            self._init_logger()

    def log(self, logtype, *texts):
        """
        creates a log message
        :param logtype: log type for the message: info, warning or error
        :param texts: different texts to be logged
        :return:
        """
        if self.logging:
            text = " ".join(texts)
            if logtype.lower() == "info":
                self._logger.info(text)
            elif logtype.lower() == "warning":
                self._logger.warning(text)
            elif logtype.lower() == "error":
                self._logger.error(text)
            else:
                self._logger.warning("message type incorrect. Message: " + text)

    def add_event_listener(self, type, button, func, funcparams, cooldown=100):
        """
        adds event listener to the event manager
        :param type:
        :param button:
        :param func:
        :param funcparams:
        :param cooldown:
        :return:
        """
        if type == "click":
            self._eventmanager.add_click_listener(button, func, funcparams, cooldown)
        if type == "keyboard":
            self._eventmanager.add_keyboard_listener(button, func, funcparams, cooldown)
        else:
            self.log("warning", "eventlistener type not know, listener not created.")
        
    def create_scene(self, sceneid:int, sceneareas=None):
        """
        creates a scene
        :param sceneid:
        :param sceneareas:
        :return:
        """
        return self._displaymanager.create_scene(sceneid, sceneareas)

    def get_data(self, datapath):
        """
        gets data from the datamanager. if the data file was not loaded, it will load it automatically
        :param datapath:
        :return:
        """
        return self._datamanager[datapath]

    def get_scene(self, sceneid):
        """
        returns scene with scene id
        :param sceneid:
        :return:
        """
        return self._displaymanager[sceneid]

    def get_config(self):
        """
        returns the engine configuration loaded at the engine startup
        :return:
        """
        return self.config
        
    def e_add_updatedentity(self, entity):
        self.updatedict[entity.entityID] = weakref.ref(entity)
        
    def e_del_updatedentity(self, entity):
        del self.updatedict[entity.entityID]


    def quit(self):
        self.log("info", "quitting")
        self.log("info", "_____________________________ ENGINE QUIT _____________________________ \n")
        self.logging = 0
        logging.shutdown()
        pg.quit()
        sys.exit()


ENGINE = Engine()
