from gevent import monkey; monkey.patch_all()
import gevent
import collections

class PeriodSelector:
    units = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600
    }
    def __init__(self, clock, func):
        self.clock = clock
        self.func = func
    
    def every(self, n, unit = 'seconds', once = False):
        if type(n) is str:
            n, unit = 1, n + 's'
        return self.clock.addCallback(n * self.units[unit], self.func, once)
        
    def inTheNext(self, n, unit = 'seconds'):
        return self.every(n, unit, True)

class ClockController:
    def __init__(self, func, once = False):
        self.func = func
        self.active = True
        self.once = once
    
    def stop(self):
        self.active = False
        
    def __repr__(self):
        return self.func.__name__ + '(%s)' % ('A' if self.active else 'X')
        
class Clock:
    def __init__(self):
        self.tick = 0
        self.func_map = collections.defaultdict(list)
    
    def start(self):
        gevent.spawn(self.run)
        gevent.sleep(0)
        
    def run(self):
        while True:
            gevent.sleep(1)
            self.every_tick()
            
    def every_tick(self):
        self.tick += 1
        #print self.tick, self.func_map
        for period, callbacks in self.func_map.items():
            callbacks_copy = callbacks[:] # avoids in loop editing
            
            if self.tick % period == 0:
                toremove = []
                for callback in callbacks_copy:
                    if callback.active:
                        callback.func()
                        if callback.once:
                            callback.active = False
                    else:
                        toremove.append(callback)
                        
            
                #if period == 60:
                #    print callbacks, "-", toremove    
                for cb in toremove:
                    self.func_map[period].remove(cb)
                #if period == 60:
                #    print self.func_map[period]

    def do(self, func):
        return PeriodSelector(self, func)
    
    def addCallback(self, seconds, func, once = False):
        control = ClockController(func, once)
        self.func_map[seconds].append(control)
        return control