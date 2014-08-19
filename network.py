from flask import Flask
from flask_sockets import Sockets
import player, format
from behaviours.player import DefaultPlayerBehaviour

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import gevent.monkey; gevent.monkey.patch_all()
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
sockets = Sockets(app)

class Connection(object):
    def __init__(self, ws):
        self.ws = ws
        self.player = None
    
    def handleLogin(self):
        self.send('Wat is jouw naam?')
        name = self.receive()
        self.send('%s. Dat is een mooie naam.' % name)
        self.player = player.Player(name)
        return self.player

    def handleMessages(self, callback):
        while True:
            message = self.ws.receive()
            if message is None:
                return
            else:
                callback(self.player, message)
    def send(self, *args, **kwargs):
        return self.ws.send(*args, **kwargs)
        
    def receive(self):
        return self.ws.receive()
        
class Server(object):
    def __init__(self, callback, behaviourFactory):
        self.connections = {}
        self.behaviourFactory = behaviourFactory
        self.callback = callback
        with open('data/welcome.txt') as f:
            self.welcome = f.read()
        with open('data/instructions.txt') as f:
            self.instructions = f.read()
        
    def addConnection(self, connection):
        self.connections[connection.player.name] = connection
    
    def removeConnection(self, connection):
        del self.connections[connection.player.name]

    def __getitem__(self, name):
        return self.getConnection(name)
        
    def getConnection(self, name):
        return self.connections[name]
        
    def run(self):
        # We could put a telnet server in here as well
        @sockets.route('/sock')
        def sock(ws):
            connection = Connection(ws)
            connection.send(self.welcome)
            player = connection.handleLogin()
            connection.send(self.instructions)
            connection.receive()
            b = self.behaviourFactory.create(player, 'behaviours.player.DefaultPlayerBehaviour')
            player.attachBehaviour(b)
            self.addConnection(connection)
            player.move('hoofdingang')
            connection.handleMessages(self.callback)
            player.logout()
            self.removeConnection(connection)

        @app.route('/')
        def index():
            return app.send_static_file('index.html')
        
        http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
        http_server.serve_forever()
