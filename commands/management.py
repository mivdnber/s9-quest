import base
class reload(base.Command):
    def run(self, net, world, player, cmd, what):
        if what == 'commands':
            self.manager.loadCommands()