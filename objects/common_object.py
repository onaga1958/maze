class Object:
    "это обычный предмет"
    pass

OBJECTS = {}


def register_object(name, cls=None):
    def helper(cls):
        OBJECTS[name] = cls
        return cls
    if cls is None:
        return helper
    else:
        return helper(cls)

register_object("сокровище", Object)
