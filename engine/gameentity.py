import weakref
from engine.funcs import *


class GameEntity:
    """
    Base class of all game entities. Each game entity as access to the engine.
    If the Engine was not initialized, no objects will be created. Each game entity
    has an automatic distributed ID.
    Each entity is added in a dictionary with their entity id.
    """
    engine = None
    _nbentity = 0
    _register=1
    _subclassdict = {}
    _cls_name = None
    _entities = {}

    def __init_subclass__(cls, **kwargs):
        cls._cls_name = cls.__name__
        if cls._register:
            cls._subclassdict[cls._cls_name]=cls
        cls.init_class()

    def __new__(cls, *args, **kwargs):
        if GameEntity.engine is None:
            return None
        else:
            return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self.entityID = GameEntity._nbentity
        GameEntity._nbentity += 1
        GameEntity.add_entity(self)
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
            self.engine.e_add_updatedentity(self)
            self._update = True
        if not value:
            self.engine.e_del_updatedentity(self)
            self._update = False

    def delete(self):
        pass

    def __del__(self):
        self.engine.log("info","Gamentity deleted:", str(type(self)))
        if self._update:
            self.engine.e_del_updatedentity(self)

    @classmethod
    def init_class(cls):
        pass

    @classmethod
    def set_subclasses(cls):
        """
        Gets all the classes that inherits from class. This function can be called in
        """
        cls.subclassdict = get_subclasses(cls)

    @classmethod
    def get_subclasses(cls):
        return cls._subclassdict

    @classmethod
    def e_set_engine(cls, engine):
        cls.engine = engine

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def set_name(cls, name):
        """
        Sets the name of the class for the engine
        """
        if name not in cls._subclassdict:
            if cls._register:
                del cls._subclassdict[cls._cls_name]
                cls._cls_name = name
                cls._subclassdict[cls._cls_name] = cls
            else:
                cls._cls_name = name
        else:
            cls.engine.log("error", "can't set name, class name already exists.")

    @classmethod
    def add_entity(cls, entity):
        cls._entities[entity.entityID] = entity

    @classmethod
    def get_entity(cls, entityid):
        return cls._entities[entityid]


class GameEntityContainer:
    pass