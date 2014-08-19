from behaviours import Behaviour
import format

class DefaultPlayerBehaviour(Behaviour):
    def __init__(self, parent, net, world):
        Behaviour.__init__(self, parent, net, world)
        
    def entityMoved(self, oldRoomId):
        if oldRoomId:
            oldRoom = self.world.getRoom(oldRoomId)
            oldRoom.removeEntity(self.parent)
        #print self.world
        newRoom = self.world.getRoom(self.parent.position)
        for line in ['','',''] + format.formatRoom(newRoom):
            print line
            self.send(line)
        newRoom.addEntity(self.parent)
        
    def entityEnteredRoom(self, entity):
        self.send('%s komt de kamer binnen' % entity.name)
    
    def entityLeftRoom(self, entity):
        self.send('%s heeft de kamer verlaten' % entity.name)
    
    def send(self, message):
        self.net[self.parent.name].send(message)

    def say(self, message):
        room = self.world.getRoom(self.parent.position)
        room.sayAll(self.parent, message)
    
    def getTold(self, entity, message):
        self.send('%s zegt: "%s"' % (entity.name, message))