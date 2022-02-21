def get_subclass(cls):
    return cls.__subclasses__()


def get_subclasses(cls):
    classes = {}
    for subclass in get_subclass(cls):
        subclassname = subclass.__name__
        classes[subclassname] = subclass
        if get_subclass(subclass):
            classes.update(get_subclasses(subclass))
    return classes


class GameEntity:
    """
    Base class of all game entities. Each game entity as access to the engine.
    If the Engine was not initialized, no objects will be created. Each game entity
    has an automatic distributed ID.
    Each entity is added in a dictionary.
    """
    engine = None
    _nbentity = 0
    _subclassdict = None

    def __new__(cls, *args, **kwargs):
        if GameEntity.engine is None:
            print('Engine not initialized, Object not created')
            return
        else:
            return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self.ID = GameEntity._nbentity
        GameEntity._nbentity += 1
        self._update = False
        if "update" in dir(self):
            self.set_update(True)
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def set_update(self, value):
        """
        Sets the entity _update attribute to the value. The entity is also 
        added or deleted from the engine update list.
        """
        if value:
            self.engine.add_updatedentity(self)
            self._update = True
        if not value:
            self.engine.del_updatedEntity(self)
            self._update = False

    def __del__(self):
        if self._update:
            self.engine.del_updatedentity(self)

    @classmethod
    def get_subclasses(cls):
        """
        Gets all the classes that inherits from GameEntity. This method must be called on
        the engine init.
        """
        cls._subclassdict = get_subclasses(cls)