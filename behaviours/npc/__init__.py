from behaviours import Behaviour

class NpcBehaviour(Behaviour):
    def __init__(self, parent, net, world):
        Behaviour.__init__(self, parent, net, world)
        self.moveInterval = 2
        self.path = []
        self.moveClock = None
        
    def entityMoved(self, oldRoomId):
        if oldRoomId:
            oldRoom = self.world.getRoom(oldRoomId)
            oldRoom.removeEntity(self.parent)
        newRoom = self.world.getRoom(self.parent.position)
        newRoom.addEntity(self.parent)

    def goto(self, room):
        self.moveClock = self.world.clock.do(self.__nextRoom).every(self.moveInterval, 'seconds')
        currentRoom = self.world.getRoom(self.parent.position)
        self.path = self.world.getPathBetween(currentRoom, room)
        self.leaving()
        
    def __nextRoom(self):
        try:
            nextRoomId = self.path.pop(0)
            self.parent.move(nextRoomId)
            self.entered()
        except IndexError:
            self.moveClock.stop()
            self.arrived()
    
    def entered(self): pass
    def arrived(self): pass
    def leaving(self): pass