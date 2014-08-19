import pickle
import entity

class Player(entity.Entity):
    def __init__(self, name):
        entity.Entity.__init__(self, name, '')
        self.health = 100
        self.nerdyness = 20
        self.inventory = []
    
    def save(self):
        pass
        
    def logout(self):
        pass