import inspect, glob, os, sys, traceback, logging

class CommandManager:
    def __init__(self, net, world):
        sys.path.append('commands')
        self.net = net
        self.world = world
        self.commands = {}
        
    def loadCommands(self):
        self.commands = {}
        for module_file in glob.glob('commands/*.py'):
            _, filename = os.path.split(module_file)
            module_name, _ = os.path.splitext(filename)
            if module_name.startswith('__') or module_name == 'base': continue
            module = __import__(module_name)
            reload(module)
            classes = inspect.getmembers(module, inspect.isclass)
            logging.info('Found %d command classes in %s', len(classes), module_name)
            for command_name, command_class in classes:
                command = command_class(self)
                for name in [command_name] + command.aliases(): 
                    self.commands[name.lower()] = command
    
    def execute(self, player, line):
        try:
            command, rest = line.split(' ', 1)
        except ValueError:
            command, rest = line, ''
        try:
            self.commands[command.lower()].execute(self.net, self.world, player, line)
            return True
        except KeyError:
            return False
        except:
            traceback.print_exc()
        return False