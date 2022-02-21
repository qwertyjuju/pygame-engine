import json
import pygame as pg
from pathlib import Path
from gameobjects import Scene


class DisplayManager:
    def __init__(self, engine):
        self.engine = engine
        self.scenes = {}
        try:
            self.engine['settings']['screensize']
        except KeyError:
            self.screensize = (900, 900)
        else:
            self.screensize = self.engine['settings']['screensize']
        self.screen = pg.display.set_mode(self.screensize)
        self.caption = "pygame"

    def set_caption(self, caption):
        self.caption = str(caption)

    def create_subsurface(self, area):
        return self.screen.subsurface(area)
        
    def update(self):
        pg.display.set_caption(self.caption)
        pg.display.flip()
        self.screen.fill((0, 0, 0))

    def create_scene(self, sceneid):
        if sceneid not in self.scenes:
            return Scene(sceneid)

    def _add_scene(self, scene):
        self.scenes[scene.id] = scene

    def _del_scene(self):
        pass

    def __getitem__(self, index):
        return self.scenes[index]
        

class DataManager:
    """
    Data Manager. All game data is stored in the data manager
    """

    def __init__(self, engine, configfile=None):
        self.engine = engine
        self.configfile = configfile
        self.files = {}
        self.data = {}
        self.mainPath = Path.cwd()
        self.set_path(self.mainPath)
        self.engine.log("info", "Datamanager initialised")
        
    def set_path(self, search_path):
        for path in search_path.iterdir():
            relative_path = str(path.relative_to(self.mainPath))
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
            raise FileNotFound()
        else:
            self._load(path_name)
        if get:
            return self.data[path_name]
            
    def _load(self, name):
        path = self.files[name]
        ext = path.suffix
        data = None
        if ext == '.json':
            with path.open('r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        if ext == '.png':
            data = GameImage(path)
        if data:
            self.data[name] = data
            self.engine.log("info", "file : "+ name + "loaded successfully")
        
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


class GameImage:
    image = None

    def __init__(self, imageloc):
        self.loc = imageloc
        self.load()
    
    def load(self):
        self.image = pg.image.load(self.loc).convert_alpha()
        
    def get_tile(self, x, y, size):
        newsurf = pg.Surface(size, pg.SRCALPHA).convert_alpha()
        newsurf.blit(self.image, (-x, -y))
        return newsurf


class DataManagerException(Exception):

    def __init__(self, message=None):
        if message:
            super().__init__(message)
        else:
            super().__init__()


class FileNotFound(DataManagerException):
    _message = 'File not in files dictionnary of data manager'

    def __init__(self, filename=None):
        if filename:
            super().__init__(FileNotFound._message+filename)
        else:
            super().__init__(FileNotFound._message)


class DirectoryNonExistent(DataManagerException):
    _message = "Directory not found. Process stopped"

    def __init__(self, dirname=None):
        if dirname:
            super().__init__(DirectoryNonExistent._message + dirname)
        else:
            super().__init__(DirectoryNonExistent._message)


"""
class EventManager(Manager):
    def init(self):
        self.signals={}
        self.listenedevents = self.signals.keys()
        
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.engine.quit()
            if event.type== pg.KEYDOWN:
                if event.key in self.listenedevents:
                    self.listeners[event.key]
    
    def add_signal(self,listener):
        self.signals[signal.keycode]= signal
        
        
        
class Signal:
    keynamelist =[
        'backspace',
        'tab',
        'clear',
        'return',
        'pause',
        'escape',
        'space',
        'exclaim',
        'quotedbl',
        'hash',
        'dollar',
        'ampersand',
        'quote',
        'left parenthesis',
        'right parenthesis',
        'asterisk',
        'plus sign',
        'comma',
        'minus sign',
        'period',
        'forward slash',
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
        'colon',
        'semicolon',
        'less-than sign',
        'equals sign',
        'greater-than sign',
        'question mark',
        'at',
        'left bracket',
        'backslash',
        'right bracket',
        'caret',
        'underscore',
        'grave',
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
        'keypad period',
        'keypad divide',
        'keypad multiply',
        'keypad minus',
        'keypad plus',
        'keypad enter',
        'keypad equals',
        'up arrow',
        'down arrow',
        'right arrow',
        'left arrow',
        'insert',
        'home',
        'end',
        'page up',
        'page down',
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
        'scrollock',
        'right shift',
        'left shift',
        'right control',
        'left control',
        'right alt',
        'left alt',
        'right meta',
        'left meta',
        'left Windows key',
        'right Windows key',
        'mode shift',
        'help',
        'print screen',
        'sysrq',
        'break',
        'menu',
        'power',
        'Euro',
    ]
    
    def __new__(cls,*args,**kwargs):
        try:
            args[0].keydict[args[1]]
        except KeyError:
            print('Signal not created, keyname not in list')
        else:
            return super().__new__(cls)
    def __init__(self,manager,eventname):
        self.manager =manager
        self.keycode= pg.key.keycode(eventname)
        self.connections={}
        self.manager.add_signal(self)
        
    def connect(self,func, *paramlist):
        self.connections[func]
    
    def activate(self):
        for func in self.connections:
            func()
            
            
class DataManager(Manager):
    def init(self, configfilepath):
        self.files = {}
        self.data = {}
        self.createfile(configfilepath,'_config',load=True)
        
    def init_config(self):
        self.config = self.get_data('_config')
        config = self.config['DataConfig']
        try:
            config['_preload']
        except KeyError:
            print('no preload instructions, no file preloaded')
        else:
            for path in config['_preload']:
                self.createfile(path,load=True)
        
            
    def createfile(self, filepath, customfilename= None, load = False):
        file = GameFile(self,filepath, customfilename)
        if load:
            self.loadfile(file.name)

    def addfile(self, file):
        try:
            self.files[file.name]
        except KeyError:
            pass
        else:
            print('file already exists. It will be replaced by new file')
        self.files[file.name]= file
        
    
    def loadfile(self, filename):
        self.files[filename].load()
    
    def add_data(self, file, data):
        try:
            self.data[file.name]
        except KeyError:
            pass
        else:
            print('data already loaded for file:',name, datatype,'the content will be replaced by new data')
        self.data[file.name] = data
                
    def __delitem__(self, index):
        try:
            self.data[index]
        except KeyError:
            print('File not found, not deleted:', index)
        else:
            del self.data[index]
            print('File deleted:', index)

    def __getitem__(self, index):
        try:
            self.data[index]
        except KeyError:
            print('Data not loaded. Check if file was correctly loaded')
            return
        else:
            return self.data[index]
"""