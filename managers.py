import pygame as pg
from gameentity import GameEntity
from gamefiles import GameFile
from scene import Scene

class Manager(GameEntity):
    def __init__(self, *args, **kwargs):
        super().__init__()
        try:
            self.init
        except AttributeError:
            pass
        else:
            self.init(*args,**kwargs)
            

class DisplayManager(Manager):
    def init(self):
        self.settings = self.get_data('_config')
        self.screensize = self.settings['Settings']['screensize']
        self.screen = pg.display.set_mode(self.screensize)
        self.caption = "pygame"
        
    def update(self):
        pg.display.set_caption(self.caption)
        pg.display.flip()
        self.screen.fill((0,0,0))
        
    def set_caption(self, caption):
        self.caption = str(caption)
    
    def createsubsurface(self,area):
        return self.screen.subsurface(area)
        
        
class SceneManager(Manager):
    def init(self):
        self.data= self.get_data('scenes.json')
        self.scenes= {}
        for sceneparams in self.data['scenes']:
            sceneparams['manager'] =self
            Scene(**sceneparams)
        try:
            self.scenes[0]
        except KeyError:
            print('ERROR: No scene ID 0.')
        else:
            self.activescene = 0
        self.scenes[self.activescene].init()
            
    def update(self):
        self.scenes[self.activescene].run()
    
    def add_scene(self, scene):
        self.scenes[scene.ID]= scene
        
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
        