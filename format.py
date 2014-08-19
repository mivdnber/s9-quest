# -*- coding: utf-8 -*-
import textwrap
import collections
def exitsMap(exits):
    repl = collections.defaultdict(lambda: u'═')
    repl['w'] = u'║'; repl['o'] = u'║'
    repl['to'] = ' '; repl['ta'] = ' '
    dspec = lambda d: d if d in exits else repl[d] * len(d)
    doors = lambda *ds: tuple([dspec(d) for d in ds])

    return [
        u'╔%s═%s═%s╗' % doors('nw', 'n', 'no'),
        u'║ %s %s ║' % doors('to', 'ta'),
        u'%s       %s' % doors('w', 'o'),
        u'║       ║',
        u'╚%s═%s═%s╝' % doors('zw', 'z', 'zo')
    ]

def mergeLines(*lineLists):
    maxLines = max(len(lineList) for lineList in lineLists)
    for lineList in lineLists:
        lineList += [''] * (maxLines - len(lineList))
    return [' '.join(lineParts) for lineParts in zip(*lineLists)]
    
def formatRoom(room):
    desc = textwrap.wrap(room.description, 70)
    # desc_70: 70 wide description next to the map
    desc_70, rest = desc[:3], desc[3:]
    # desc_80: 80 wide description below the map
    desc_80 = textwrap.wrap('\n'.join(rest), 80)
    
    ret = mergeLines(
        exitsMap(room.exits),
        [
            room.title,
            '=' * len(room.title)
        ] + desc_70
    ) + desc_80

    present = [e.name for e in room.getEntities() if not e.presenceString]
    if present: ret += ['\nAanwezig: ' + ', '.join(present)]
    for entity in room.getEntities():
        if entity.presenceString:
            ret += [entity.presenceString + '\n']
    return ret