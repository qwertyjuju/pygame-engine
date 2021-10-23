
def get_subclass(cls):
    return cls.__subclasses__()

def get_subclasses(cls):
    classes={}
    for subclass in get_subclass(cls):
        subclassname = subclass.__name__
        classes[subclassname]= subclass
        if get_subclass(subclass):
            classes.update(get_subclasses(subclass))
    return classes

class GameEntity:
    """
    Base class of all game entitys. Each game entity as acces to the engine.
    If the Engine was not initialized, no onjects will be created. Each game entity
    has an automatic distributed ID.
    """
    engine = None
    nbentity = 0
    entitydict = None
    events = None

    def __new__(cls, *args, **kwargs):
        if GameEntity.engine == None:
            print('Engine not initialized, Object not created')
            return
        else:
            return super().__new__(cls)
    
    def __init__(self):
        self.engine = GameEntity.engine
        self._ID= GameEntity.nbentity
        GameEntity.nbentity+=1
        self.statedict= {
            'update': False,
        }
        try:
            self.update
        except AttributeError:
            pass
        else:
            self.statedict['update'] = True
            
    def run(self):
        self.events = GameEntity.events
        self.__update__()
        
    def __update__(self):
        if self.statedict['update']:
            self.update()
            
    def get_data(self,dataname):
        try:
            self.engine.datamanager[dataname]
        except KeyError:
            print('data not found. File was not loaded')
            return
        else:
            return self.engine.datamanager[dataname]
        
    def remove_data(self, dataname):
        pass
        
    @classmethod    
    def get_subclasses(cls):
        cls.entitydict = get_subclasses(cls)
                        

        