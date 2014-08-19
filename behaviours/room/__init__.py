from behaviours import Behaviour

class DefaultRoomBehaviour(Behaviour):
    def sayAll(self, player, message):
        doAfter = []
        for entity in self.parent.getEntities():
            cb = entity.getTold(player, message)
            if cb:
                doAfter.append(cb)
        for cb in doAfter: cb()
        
    def sendAll(self, player, message):
        doAfter = []
        for entity in self.parent.getEntities():
            cb = entity.call('send', message)
            if cb:
                doAfter.append(cb)
        for cb in doAfter: cb()