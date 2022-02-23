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