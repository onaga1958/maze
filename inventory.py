class Object:
    def __init__(self, name):
        self.name = name
        self.count = 1

OBJECTS = {}

def register_object(name, cls=None):
    def helper(cls):
        OBJECTS[name] = cls
        return cls
    if cls is None:
        return helper
    else:
        return helper(cls)

class Inventory:
    def __init__(self, objects=None):
        if objects:
            if isinstance(objects, Inventory):
                objects = objects.objects
            self.objects = objects
        else:
            self.objects = {}

    def add(self, obj):
        if obj in self.objects:
            self.objects[obj] += 1
        else:
            self.objects[obj] = 1

    def remove(self, obj):
        if obj.name not in self.objects:
            raise KeyError()
        self.objects[obj] -= 1
        if self.objects[obj] == 0:
            del self.objects[obj]

    def count(self, obj):
        return self.objects.get(obj, 0)
    
    def __str__(self):
        if not self:
            return "ничего"
        tmp = []
        for k, v in self.objects.items():
            if v == 1:
                tmp.append(k)
            else:
                tmp.append("{}x{}".format(k, v))
        return ", ".join(tmp)

    def update(self, inv):
        self.objects.update(inv.objects)

    def __contains__(self, key):
        return key in self.objects
    
    def action(self, game, player, action):
        obj, action = action.split()
        if obj not in self.objects:
            raise KeyError()
        is_used = obj.action(game, player, action)
        if is_used:
            self.remove(obj)

    def __bool__(self):
        return bool(self.objects)
