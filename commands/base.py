import inspect
import glob, os, sys
        
class Command:
    def __init__(self, manager):
        self.manager = manager
        
    def execute(self, net, world, player, input):
        try:
            command, rest = input.split(' ', 1)
        except:
            print 'single word command'
            command, rest = input, ''
        print rest.split(' ')
        self.run(net, world, player, command, *rest.split(' '))
        
    def run(self, net, world, player, command, *rest):
        pass
        
    def aliases(self):
        return []