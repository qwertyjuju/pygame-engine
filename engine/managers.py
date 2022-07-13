from pathlib import Path
import pygame as pg
from engine.gameobjects import Scene
from engine.gameexceptions import *
import engine.loadfuncs as lf
import time


class Manager:
    engine = None

    def __init__(self, *args, **kwargs):
        self.init(*args,**kwargs)

    def init(self, *args,**kwargs):
        pass

    @classmethod
    def e_set_engine(cls, engine):
        cls.engine = engine


class DisplayManager(Manager):
    def init(self, screensize= None):
        self.screensize = screensize if screensize is not None else (900, 900)
        self.screen = pg.display.set_mode(self.screensize)
        self.scenes = {}
        self._active_scene = None
        self.caption = "pygame"
        self.init_scenes()
        self.engine.log("info", "Display Manager initialised. \n screensize :", str(self.screensize), "\n scenes :", str(self.scenes))

    def init_scenes(self):
        config=self.engine.get_config()
        if 'scenes' in config:
            if config['scenes']:
                self.scenesdata = self.engine.get_data(config['scenes'])
                self.engine.log("info", "scenes data:", str(self.scenesdata))
                for scenedata in self.scenesdata["scenes"]:
                    self.create_scene(scenedata["ID"], scenedata["SceneAreas"])
        else:
            self.engine.log("warning", "No scene file given in engine settings")

    def set_caption(self, caption):
        self.caption = str(caption)
        
    def update(self):
        pg.display.set_caption(self.caption)
        if self._active_scene:
            for area in self._active_scene.get_areas().values():
                area.render()
        pg.display.flip()

    def create_scene(self, sceneid, sceneareas=None):
        if sceneid not in self.scenes:
            return Scene(self, sceneid, sceneareas)
        else:
            self.engine.log("error", "Scene not created, sceneID already exists. SceneID:", sceneid)

    def e_set_active_scene(self, scene):
        if self._active_scene is not None:
            self._active_scene.e_deactivate()
            self._active_scene = scene
        else:
            self._active_scene = scene

    def e_add_scene(self, scene):
        self.scenes[scene.id] = scene

    def __getitem__(self, index):
        return self.scenes[index]


class DataManager(Manager):
    """
    Data Manager. All game data is stored in the data manager
    """
    _loadfuncs = lf.LOADFUNCS

    def init(self, configfile=None):
        self.configfile = configfile
        self.data = {}
        self.mainPath = Path.cwd()

    def set_path(self, pathname):
        search_path = Path(pathname)
        if search_path.exists():
            for path in search_path.iterdir():
                if path.is_dir():
                    self.set_path(path)
                elif path.is_file():
                    self.data[path] = None
            print(self.data)
        else:
            self.engine.log("warning", f"Path: {pathname} not found, path not set in datamanager")

    def load(self, pathname):
        path = Path().joinpath(*pathname.split("|"))
        if path not in self.data.keys():
            raise FileNotFound(path)
        else:
            if not self.data[path]:
                self._load(path)
            return self.data[path]

    def _load(self, path):
        ext = path.suffix
        data = None
        if ext in self._loadfuncs.keys():
            try:
                data = self._loadfuncs[ext](path)
            except Exception as e:
                self.engine.log("error", f"file : {path} - loaded unsuccessfully, {e}")
        else:
            self.engine.log("warning", f"{ext} extension not know, file: {path} not loaded")
        if data:
            self.engine.log("info", f"file : {path} - loaded successfully")
        else:
            self.engine.log("warning", f"file : {path} - no data loaded")
        self.data[path] = data

    def save(self, pathname):
        path = Path(pathname)
        if path not in self.data.keys():
            raise FileNotFound()
        else:
            self._save(path)

    def _save(self, path):
        ext = path.suffix
        if ext == '.json':
            lf.save_json(path, self.data[path])

    def __getitem__(self, pathname):
        return self.load(pathname)

    def __setitem__(self, pathname, value):
        path = Path(pathname)
        if path not in self.data.keys():
            raise FileNotFound()
        else:
            self.data[path] = value
            self._save(path)


class EventManager(Manager):
    keynamelist = [
        'backspace',
        'tab',
        'clear',
        'return',
        'pause',
        'escape',
        'space',
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        'delete',
        'keypad 0',
        'keypad 1',
        'keypad 2',
        'keypad 3',
        'keypad 4',
        'keypad 5',
        'keypad 6',
        'keypad 7',
        'keypad 8',
        'keypad 9',
        'up',
        'down',
        'right',
        'left',
        'insert',
        'home',
        'end',
        'F1',
        'F2',
        'F3',
        'F4',
        'F5',
        'F6',
        'F7',
        'F8',
        'F9',
        'F10',
        'F11',
        'F12',
        'F13',
        'F14',
        'F15',
        'numlock',
        'capslock',
        'right shift',
        'left shift',
        'right ctrl',
        'left ctrl',
        'right alt',
        'left alt',
        'help',
    ]

    def init(self):
        Listener.e_set_manager(self)
        self._listeners = {
            "click": {
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
            },
            "keyboard": {keynb: [] for keynb in [pg.key.key_code(keyname) for keyname in self.keynamelist]}
        }
        self._updatelist = []
        self.time = 0
        self.clock = pg.time.Clock()

    def update(self):
        self.time += self.clock.tick()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.engine.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button in self._listeners["click"]:
                    for listener in self._listeners["click"][event.button]:
                        listener.activate()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in self._listeners["click"]:
                    for listener in self._listeners["click"][event.button]:
                        listener.deactivate()
            if event.type == pg.KEYDOWN:
                if event.key in self._listeners["keyboard"]:
                    for listener in self._listeners["keyboard"][event.key]:
                        listener.activate()
            if event.type == pg.KEYUP:
                if event.key in self._listeners["keyboard"]:
                    for listener in self._listeners["keyboard"][event.key]:
                        listener.deactivate()

        for listener in self._updatelist:
            listener.update()

    def add_click_listener(self, button, func, funcparams, cooldown):
        if button in range(1,6):
            self._listeners["click"][button].append(Listener(func, funcparams, cooldown))
        else:
            self.engine.log("warning", f"eventlistener button, {button}, not know, listener not created.")

    def add_keyboard_listener(self, button, func, funcparams, cooldown):
        if button in self.keynamelist:
            self._listeners["keyboard"][pg.key.key_code(button)].append(Listener(func, funcparams, cooldown))
        else:
            self.engine.log("warning", "eventlistener button, {button}, not know, listener not created.")


    def add_to_updatel(self, listener):
        self._updatelist.append(listener)

    def del_to_updatel(self, listener):
        self._updatelist.remove(listener)


class Listener:
    manager = None

    def __init__(self, func, funcparams=None, cooldown=100):
        self._active = 0
        self.func = func
        self.params = funcparams
        self.cooldown = cooldown

    def activate(self):
        if not self._active:
            self.func(*self.params)
            self.t_update = self.manager.time
            self.manager.add_to_updatel(self)
            self.active = 1

    def deactivate(self):
        self.manager.del_to_updatel(self)
        self.active = 0

    def update(self):
        if self.manager.time-self.t_update >= self.cooldown:
            self.func(*self.params)
            self.t_update = self.manager.time

    @classmethod
    def e_set_manager(cls, manager):
        cls.manager = manager


"""
            if event.type == pg.QUIT:
                self.engine.quit()
            if event.type == pg.KEYDOWN:
                pass
            if event.type == pg.KEYUP:
                pass
            if event.type == pg.MOUSEMOTION:
                pass
"""