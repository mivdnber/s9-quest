# -*- coding: utf-8 -*-
from behaviours.npc import NpcBehaviour

import itertools
import textwrap
import random

class Gunnar(NpcBehaviour):
    deutschland = itertools.cycle(textwrap.dedent(u'''
    Deutschland, Deutschland über alles
    über alles in der Welt,
    wenn es stets zu Schutz und Trutze
    brüderlich zusammenhält.
    Von der Maas bis an die Memel,
    von der Etsch bis an den Belt,
    Deutschland, Deutschland über alles,
    über alles in der Welt!
    Deutsche Frauen, deutsche Treue,
    deutscher Wein und deutscher Sang
    sollen in der Welt behalten
    ihren alten schönen Klang,
    uns zu edler Tat begeistern
    unser ganzes Leben lang.
    Deutsche Frauen, deutsche Treue,
    deutscher Wein und deutscher Sang!
    Einigkeit und Recht und Freiheit
    für das deutsche Vaterland!
    Danach lasst uns alle streben
    brüderlich mit Herz und Hand!
    Einigkeit und Recht und Freiheit
    sind des Glückes Unterpfand;
    blüh' im Glanze dieses Glückes,
    blühe, deutsches Vaterland.''').split('\n'))
    
    def attached(self):
        self.singClock = self.world.clock.do(self.sing).every(3, 'seconds')
        pass
        
    def entityEnteredRoom(self, entity):
        room = self.world.getRoom(self.parent.position)
        room.call('sayAll', self.parent, 'Gutentag, %s!' % entity.name)
        
    def sing(self):
        room = self.world.getRoom(self.parent.position)
        room.call('sayAll', self.parent, u'♫ %s ♫' % self.deutschland.next())
        
    def getTold(self, entity, message):
        if 'zwijg' in message:
            self.singClock.stop()
            room = self.world.getRoom(self.parent.position)
            def answer():
                room.call('sayAll', self.parent, 'OK %s!' % entity.name)
            return answer

class KrisCoolsaet(NpcBehaviour):
    def attached(self):
        self.specialClock = self.world.clock.do(self.gotoRandomRoom).every(10, 'minutes')
        
    def gotoRandomRoom(self):
        currentRoom = self.world.getRoom(self.parent.position)
        randomRoom = currentRoom
        while randomRoom is currentRoom:
            randomRoom = random.choice(self.world.getRooms())
        self.goto(randomRoom)
        
    def arrived(self):
        room = self.world.getRoom(self.parent.position)
        room.call('sayAll', self.parent, 'Mmm, een while met dubbele conditie!')
