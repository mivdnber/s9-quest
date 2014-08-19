import sys

import world, player, command, entity, network
import format, clock
import behaviours
from behaviours.room import DefaultRoomBehaviour
from behaviours.npc.profs import Gunnar, KrisCoolsaet

import logging

from gevent.fileobject import FileObject
sys.stdin = FileObject(sys.stdin)

class MainProgram(object):
    def __init__(self):
        behaviourFactory = behaviours.BehaviourFactory()
        self.world = world.World(behaviourFactory)
        self.server = network.Server(self.messageReceived, behaviourFactory)
        behaviourFactory.initialize(self.server, self.world)
        self.world.load('data/s9.tgf')
        
        for room in self.world.getRooms():
            room.attachBehaviour(DefaultRoomBehaviour(room, self.server, self.world))

        self.commandManager = command.CommandManager(self.server, self.world)
        self.commandManager.loadCommands()
        #self.addNpcs()
        
    def addNpcs(self):
        gunnar = entity.Entity('Gunnar Brinkmann', presenceString = 'Prof. dr. Gunnar Brinkmann')
        gunnar.attachBehaviour(Gunnar(gunnar, self.server, self.world))
        gunnar.move('a0')
        
        coolsaet = entity.Entity('Kris Coolsaet', presenceString = 'Prof. dr. Kris Coolsaet')
        coolsaet.attachBehaviour(KrisCoolsaet(coolsaet, self.server, self.world))
        coolsaet.move('hoofdinkom')
        pass
        
    def messageReceived(self, player, message):
        if not message: return
        if not self.commandManager.execute(player, message):
            self.commandManager.execute(player, 'zeg %s' % message)
        
    def run(self):
        self.world.run()
        self.server.run()

def main(argv):
    logging.basicConfig(level = logging.DEBUG)
    program = MainProgram()
    program.run()
    
if __name__ == '__main__':
    main(sys.argv)