class Behaved(object):
    def __init__(self):
        self.behaviours = []
    
    def attachBehaviour(self, behaviour):
        behaviour.parent = self
        self.behaviours.append(behaviour)
        behaviour.attached()
        
    def detachBehaviour(self, behaviour):
        self.behaviours.remove(behaviour)
        behaviour.detached()
        
    def __getBehaviourMethod(self, name):
        for behaviour in self.behaviours[:]:
            if hasattr(behaviour, name):
                return getattr(behaviour, name)
        return lambda *args, **kwargs: None
                
    def call(self, name, *args, **kwargs):
        return self.__getBehaviourMethod(name)(*args, **kwargs)
                
    def __getattr__(self, name):
        return self.__getBehaviourMethod(name)

class Entity(Behaved):
    def __init__(self, name, description='', position=None, presenceString=None):
        Behaved.__init__(self)
        self.name = name
        self.description = description
        self.position = position
        self.presenceString = presenceString
        
    def move(self, room):
        oldRoom = self.position
        self.entityMoving(oldRoom, room)
        self.position = room
        self.entityMoved(oldRoom)
