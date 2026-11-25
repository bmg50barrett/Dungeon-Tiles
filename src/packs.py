"""Room Packs: one-sheet files of the room layouts dungeons use most, to print as many times as a dungeon needs.

The full room sets carry every layout a few times each, spread over several sheets, so a dungeon with
eight 1-door rooms pays for a lot of rooms it doesn't use. The packs carry mostly the common layouts
(1 door, 2 opposite, 2 at a corner), weighted by what tile-mode dungeons from Dungeon Maker need, with
hallway pieces in the spare space. The rare layouts (3 and 4 doors) still come from the full sets.

    4x4 Room Pack                 4 rooms: 1 door x2, 2 opposite, 2 at a corner
    5x5 Room Pack A               2 rooms: 1 door, 2 opposite
    5x5 Room Pack B               2 rooms: 2 at a corner, 3 doors
    4x4 Room Pack, double-sided   1/3, 1/corner, opposite/corner, opposite/4
    5x5 Room Pack, double-sided   1/corner, opposite/3

Each file is one sheet with its own cut guide."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg
from rooms import room_walls, H5
from rooms4 import pinwheel_walls

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')
NAMES = {'N': '1 door', 'NS': '2 doors, opposite', 'NE': '2 doors, corner', 'NES': '3 doors', 'NESW': '4 doors'}
SHORT = {'S4': '4 long', 'S5': '5 long', 'S1': '1 long', 'L': 'corner', 'T': 'T'}
HALL = {'S4v': (1, 4, H5['v'](4), 'S4'), 'S4h': (4, 1, H5['h'](4), 'S4'), 'S5v': (1, 5, H5['v'](5), 'S5'),
        'L': (1, 1, H5['corner'], 'L'), 'S1': (1, 1, H5['v'](1), 'S1'), 'T': (1, 1, H5['tee'], 'T')}


def r4(doors):
    return (4, 4, pinwheel_walls(doors), f"Room 4x4: {NAMES[doors]}")


def r5(doors):
    return (5, 5, room_walls(5, doors), f"Room 5x5: {NAMES[doors]}")


def hall(front, back=None):
    """A hallway piece, with an optional different face on the back (same footprint, 1x1 pieces only)."""
    w, h, fw, fk = HALL[front]
    _, _, bw, bk = HALL[back or front]
    return (w, h, fw, bw, SHORT[fk], SHORT[bk])


def room(spec, back=None):
    w, h, fw, flab = spec
    if back is None:
        return (w, h, fw, fw, flab, None)
    return (w, h, fw, back[2], flab, back[3].split(': ', 1)[1])


# spare space on a 4x4 pack: an 8 x 2 band; on a 5x5 pack: a 3 x 10 strip
def band4(smalls):
    return [(0, 8, hall('S4h')), (4, 8, hall('S4h'))] + [(i, 9, s) for i, s in enumerate(smalls)]


def strip5(smalls):
    return ([(5, 0, hall('S5v')), (6, 0, hall('S5v')), (5, 5, hall('S4v')), (6, 5, hall('S4v'))]
            + [(x, y, s) for (x, y), s in zip([(5, 9), (6, 9)] + [(7, y) for y in range(10)], smalls)])


ROOM4_AT = [(0, 0), (4, 0), (0, 4), (4, 4)]
ROOM5_AT = [(0, 0), (0, 5)]

PACKS = [
    dict(id='pack-4x4', name='4x4 Room Pack', file='4x4 Room Pack', two=False,
         items=[(x, y, room(r4(d))) for (x, y), d in zip(ROOM4_AT, ['N', 'N', 'NS', 'NE'])]
         + band4([hall('L')] * 5 + [hall('S1')] * 3)),
    dict(id='pack-5x5-a', name='5x5 Room Pack A', file='5x5 Room Pack A', two=False,
         items=[(x, y, room(r5(d))) for (x, y), d in zip(ROOM5_AT, ['N', 'NS'])]
         + strip5([hall('L')] * 8 + [hall('S1')] * 4)),
    dict(id='pack-5x5-b', name='5x5 Room Pack B', file='5x5 Room Pack B', two=False,
         items=[(x, y, room(r5(d))) for (x, y), d in zip(ROOM5_AT, ['NE', 'NES'])]
         + strip5([hall('L')] * 8 + [hall('S1')] * 4)),
    dict(id='pack-4x4-duplex', name='4x4 Room Pack, Double-Sided', file='4x4 Room Pack Double-Sided', two=True,
         items=[(x, y, room(r4(f), r4(b))) for (x, y), (f, b) in zip(ROOM4_AT, [('N', 'NES'), ('N', 'NE'), ('NS', 'NE'), ('NS', 'NESW')])]
         + band4([hall('L', 'S1')] * 5 + [hall('L', 'T')] * 3)),
    dict(id='pack-5x5-duplex', name='5x5 Room Pack, Double-Sided', file='5x5 Room Pack Double-Sided', two=True,
         items=[(x, y, room(r5(f), r5(b))) for (x, y), (f, b) in zip(ROOM5_AT, [('N', 'NE'), ('NS', 'NES')])]
         + strip5([hall('L')] * 2 + [hall('L', 'S1')] * 6 + [hall('L', 'T')] * 4)),
]


def check(items):
    occ = set()
    for x, y, p in items:
        for i in range(int(p[0])):
            for j in range(int(p[1])):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    size = (PAGE_W * inch, PAGE_H * inch)
    seed = 15000
    for pack in PACKS:
        items, two = pack['items'], pack['two']
        print(f"{pack['name']}: {check(items)} of 80 squares")
        c = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {pack['file']}.pdf"), pagesize=size)
        c.setTitle(f"Dungeon Tiles - {pack['file']}")
        header(c, f"{pack['name']}  |  {'Sheet 1 FRONT' if two else 'Print as many as you need'}")
        for x, y, (w, h, fw, bw, _, _) in items:
            floor(c, x, y, w, h, fw, seed); seed += 13
        c.showPage()
        if two:
            header(c, f"{pack['name']}  |  Sheet 1 BACK", "Back side. Print duplex, flip on long edge. The ruler must measure exactly 2 inches.")
            for x, y, (w, h, fw, bw, _, _) in items:
                floor(c, 8 - x - w, y, w, h, bw, seed); seed += 13
            c.showPage()
        c.save()
        g = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {pack['file']} Cut Guide.pdf"), pagesize=size)
        g.setTitle(f"Dungeon Tiles - {pack['file']} Cut Guide")
        label = lambda f, b: f if (b is None or b == f) else f"{f}  /  back: {b}"
        cg.draw_guide(g, f"{pack['name']} Cut Guide" + ('  |  front up' if two else ''),
                      [(x, y, w, h, label(fl, bl)) for x, y, (w, h, _, _, fl, bl) in items])
        g.showPage(); g.save()
