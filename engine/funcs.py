def get_subclass(cls):
    return cls.__subclasses__()


def get_subclasses(cls):
    classes = {}
    for subclass in get_subclass(cls):
        try:
            subclass.__cls_name__
        except AttributeError:
            subclassname = subclass.__name__
        else:
            subclassname = subclass.__cls_name__.lower()
        classes[subclassname] = subclass
        if get_subclass(subclass):
            classes.update(get_subclasses(subclass))
    return classes