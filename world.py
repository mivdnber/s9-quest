import networkx as nx
import glob
import yaml
import logging

import entity, behaviours, clock

class Room(entity.Behaved):
    def __init__(self, id, title, description, exits):
        entity.Behaved.__init__(self)
        self.entities = []
        self.id = id
        self.title = title
        self.description = description
        self.exits = exits
    
    def addEntity(self, entity):
        logging.info('adding entity %s to room %s', entity.name, self.id)
        self.entities.append(entity)
        self.entityEntered(entity)
        for otherEntity in self.getEntities():
            otherEntity.entityEnteredRoom(entity)
    
    def removeEntity(self, entity):
        logging.info('removing entity %s to room %s', entity.name, self.id)
        self.entities.remove(entity)
        self.entityLeft(entity)
        for otherEntity in self.getEntities():
            otherEntity.entityLeftRoom(entity)
        
    def getEntities(self):
        return self.entities[:]

class World(object):
    def __init__(self, behaviourFactory):
        self.behaviourFactory = behaviourFactory
        self.clock = clock.Clock()
        self.rooms = {}
    
    def load(self, path):
        self.graph = self.loadGraph(path)
        descriptions = self.loadDescriptions()
        
        for node in self.graph.nodes():
            desc = descriptions[node]
            adj = self.graph[node]
            exits = {}
            for dest, edge in adj.items():
                exits[edge['direction']] = dest
            self.rooms[node] = Room(node, desc['title'], desc['description'], exits)
            for npcDesc in (desc['npcs'] if 'npcs' in desc else []):
                npc = entity.Entity(npcDesc['name'])
                logging.info('created npc "%s"', npc.name)
                for behaviourDesc in (npcDesc['behaviours'] if 'behaviours' in npcDesc else []):
                    npc.attachBehaviour(self.behaviourFactory.create(npc, behaviourDesc['class']))
                npc.move(node)
                
        logging.info('loaded %d rooms', len(self.rooms))

    def run(self):
        self.clock.start()

    def loadDescriptions(self):
        descriptions = {}
        for path in glob.glob('data/rooms/*.yaml'):
            with open(path) as file:
                for room in yaml.load_all(file):
                    descriptions[room['id']] = room            
        return descriptions
    
    def loadGraph(self, path):
        id_mapping = {}
        graph = nx.DiGraph()
        with open(path) as file:
            readingNodes = True
            for line in file:
                if line.startswith('#'):
                    readingNodes = False
                    continue
                elif readingNodes:
                    id, label = line.replace('\n', '').replace('\r', '').split(' ', 1)
                    id_mapping[id] = label
                    graph.add_node(label)
                elif line:
                    left, right, direction = line.replace('\n', '').replace('\r', '').split(' ', 2)
                    graph.add_edge(id_mapping[left], id_mapping[right], direction = direction)
        return graph
    
    def getRoom(self, id):
        return self.rooms[id]

    def getRooms(self):
        return self.rooms.values()
        
    def getPathBetween(self, source, destination):
        return nx.shortest_path(self.graph, source.id, destination.id)[1:]
        