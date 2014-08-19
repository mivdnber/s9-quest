from behaviours import Behaviour

class Bowels(Behaviour):
    '''
    Yes, this is disgusting, but it does serve as a good example of a behaviour.
    My sincere apologies.
    '''
    def attached(self):
        self.shitClock = self.world.clock.do(self.findBathroom).inTheNext('minute')
        self.path = []
        
    def findBathroom(self):
        currentRoom = self.world.getRoom(self.parent.position)
        self.path = self.world.getPathBetween(currentRoom, self.world.getRoom('wc a0 m'))
