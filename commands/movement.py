import base
import format

class Teleporteer(base.Command):
    def run(self, net, world, player, cmd, room):
        player.move(room)
        connection = net[player.name]
        for line in format.formatRoom(world.getRoom(room)):
            connection.ws.send(line)
        
class Ga(base.Command):
    def run(self, net, world, player, cmd, *args):
        direction = ''
        connection = net[player.name]
        if cmd in self.aliases():
            direction = cmd
        else:
            direction = args[0]
        room = world.getRoom(player.position)
        if direction in room.exits:
            newRoom = room.exits[direction]
            player.move(newRoom)
        else:
            player.call('send', 'Die richting kan je niet uit')
            
        
    def aliases(self):
        return ['n', 'z', 'o', 'w', 'nw', 'no', 'zw', 'zo', 'to', 'ta']

class Kijk(base.Command):
    def run(self, net, world, player, cmd, *args):
        player.call('entityMoving', player.position, player.position)