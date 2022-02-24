from engine.funcs import *


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
    _entities = {}

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
            self.engine.add_updatedentity(self)
            self._update = True
        if not value:
            self.engine.del_updatedEntity(self)
            self._update = False

    def delete(self):
        pass

    def __del__(self):
        self.engine.log("info","Gamentity deleted:", str(type(self)))
        if self._update:
            self.engine.del_updatedentity(self)

    @classmethod
    def init_gameentity(cls):
        cls._set_subclasses()
        for gameentityclass in cls._subclassdict.values():
            gameentityclass.init_class()

    @classmethod
    def init_class(cls):
        pass

    @classmethod
    def _set_subclasses(cls):
        """
        Gets all the classes that inherits from GameEntity. This method must be called on
        the engine init.
        """
        cls._subclassdict = get_subclasses(cls)

    @classmethod
    def get_subclasses(cls):
        return cls._subclassdict

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def add_entity(cls, entity):
        cls._entities[entity.entityID] = entity
