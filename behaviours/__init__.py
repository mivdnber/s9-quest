class Behaviour(object):
    def __init__(self, parent, net, world):
        self.parent = parent
        self.net = net
        self.world = world
    
    def attached(self):
        pass
        
    def detached(self):
        pass
        
class BehaviourFactory(object):
    def __init__(self, net = None, world = None, prefix=''):
        self.initialize(net, world)
        self.prefix = prefix
        
    def initialize(self, net, world):
        self.net = net
        self.world = world
        
    def create(self, parent, path, *args, **kwargs):
        moduleName, className = path.rsplit('.', 1)
        if self.prefix:
            moduleName = self.prefix + '.' + moduleName
        module = __import__(moduleName)
        for name in moduleName.split('.')[1:]:
            module = getattr(module, name)
        
        return module.__dict__[className](parent, self.net, self.world, *args, **kwargs)
        
    def __call__(self, parent, path, *args, **kwargs):
        return self.create(parent, path, *args, **kwargs)