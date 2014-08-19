import base

class Zeg(base.Command):
    def run(self, net, world, player, cmd, *message):
        room = world.getRoom(player.position)
        room.call('sayAll', player, ' '.join(message))