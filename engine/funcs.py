def get_subclass(cls):
    return cls.__subclasses__()


def get_subclasses(cls):
    classes = {}
    for subclass in get_subclass(cls):
        try:
            subclass.cls_id
        except AttributeError:
            subclassname = subclass.__name__
        else:
            subclassname = subclass.cls_id.lower()
        classes[subclassname] = subclass
        if get_subclass(subclass):
            classes.update(get_subclasses(subclass))
    return classes