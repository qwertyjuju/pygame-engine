from pathlib import Path
import pygame as pg
from engine.gameobjects import Scene
from engine.gameexceptions import *
import engine.loadfuncs as lf


class DisplayManager:
    def __init__(self, engine):
        self.engine = engine
        if 'screensize' in self.engine:
            if self.engine['screensize'] is not None:
                self.screensize = self.engine['screensize']
            else:
                self.screensize = (900, 900)
        self.screen = pg.display.set_mode(self.screensize)
        self.scenes = {}
        self._active_scene = None
        self.caption = "pygame"
        self.init_scenes()
        self.engine.log("info", "Display Manager initialised. \n screensize :", str(self.screensize), "\n scenes :", str(self.scenes))

    def init_scenes(self):
        if 'scenes' in self.engine:
            if self.engine['scenes']:
                self.scenesdata = self.engine.get_data(self.engine['scenes'])
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
        

class DataManager:
    """
    Data Manager. All game data is stored in the data manager
    """
    _loadfuncs=lf.LOADFUNCS

    def __init__(self, engine, configfile=None):
        self.engine = engine
        self.configfile = configfile
        self.files = {}
        self.data = {}
        self.mainPath = Path.cwd()
        self.engine.log("info", "Data Manager initialised.")
        
    def set_path(self, search_path):
        search_path = self.mainPath.joinpath(Path(search_path))
        for path in search_path.iterdir():
            relative_path = path.relative_to(self.mainPath).as_posix()
            if path.is_dir():
                self.set_path(path)
            elif path.is_file():
                self.files[relative_path] = path

    def get_data(self, name):
        try:
            self.data[name]
        except KeyError:
            self.load(name)
        return self.data[name]
    
    def loads(self, *path_names):
        """
        loads several files
        """
        for path_name in path_names:
            self.load(path_name)
            
    def load(self, path_name, get=False):
        """
        loads the file passed to the function. If the path was not set, a FileNotFound error
        will be raised. if the get parameter is set to 1, the function return the data
        loaded
        """
        try:
            self.files[path_name]
        except KeyError:
            print(self.files)
            raise FileNotFound(path_name)
        else:
            self._load(path_name)
        if get:
            return self.data[path_name]
            
    def _load(self, name):
        path = self.files[name]
        ext = path.suffix
        data = None
        if ext in self._loadfuncs.keys():
            try:
                data = self._loadfuncs[ext](path)
            except Exception as e:
                self.engine.log("error", f"file : {name} - loaded unsuccessfully, {e}")
        else:
            self.engine.log("warning", f"{ext} extension not know, file: {name} not loaded")
        if data:
            self.engine.log("info", f"file : {name} - loaded successfully")
        else:
            self.engine.log("warning", f"file : {name} - no data loaded")
        self.data[name] = data

    def save(self, pathname):
        try:
            self.files[pathname]
        except KeyError:
            raise FileNotFound()
        else:
            self._save(pathname)
    
    def _save(self, name):
        path = self.files[name]
        ext = path.suffix
        with path.open('w') as file:
            if ext == '.json':
                json.dump(self.data[name], file, indent=4)
                
    def create_file(self, str_path, data=None):
        path = Path.joinpath(self.mainPath, str_path)
        parentpath = path.parent
        if not parentpath.exists():
            raise DirectoryNonExistent()
        elif parentpath.is_relative_to(self.mainPath) and not path.exists():
            path.touch()
            self.files[str_path] = path
            if data:
                self.data[str_path] = data
                self.save(str_path)
    
    def createdir(self, str_path):
        path = Path.joinpath(self.mainPath, str_path)
        parent_path = path.parent
        if not parent_path.exists():
            raise DirectoryNonExistent()
        else:
            path.mkdir()

    def exists(self, pathname):
        try:
            self.files[pathname]
        except KeyError:
            return False
        else:
            if self.files[pathname].exists():
                return True
            else:
                return False

    def __getitem__(self, index):
        try:
            self.data[index]
        except KeyError:
            self.load(index)
        return self.data[index]


class EventManager:
    def __init__(self, engine):
        self.engine = engine
        self._events = {
            "Quit": self.engine.quit,
            "KeyDown": self.keydown,
            "KeyUp": self.keyup
        }
        self._eventkeys=self._events.keys()
        self.keydown_listeners = {}

    def update(self):
        for event in pg.event.get():
            evname = pg.event.event_name(event.type)
            if evname in self._eventkeys:
                self._events[evname]()

    def add_keydown_listener(self):
        pass

    def keydown(self):
        pass

    def keyup(self):
        pass


class Listener:

    def __init__(self, manager, func, funcparams, key=None, cooldown=30):
        self.manager = manager
        self.active = 0

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