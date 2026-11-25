"""Full Rooms: ready-made 4x4 and 5x5 rooms in every door layout, with spare
space filled by 5 ft and 10 ft hallways. Also writes a matching cut guide.

Doorways are centered in their wall: 10 ft (2 squares) on 4x4 rooms, which fit
the 10 ft door strips, and 5 ft (1 square) on 5x5 rooms."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')


def room_walls(n, doors):
    """Walls for an n x n room. doors is a string of sides from 'NESW'."""
    g = 2 if n % 2 == 0 else 1
    # the opening matches a hallway's floor: the doorway square(s) keep a wall
    # stub of thickness T on each side, just like the hallway's own walls
    a, b = (n - g) / 2 + T, (n + g) / 2 - T
    rects = []
    # north and south walls run the full width
    for side, v in (('N', 0), ('S', n - T)):
        if side in doors:
            rects += [(0, v, a, T), (b, v, n - b, T)]
        else:
            rects.append((0, v, n, T))
    # east and west walls fit between them
    for side, u in (('W', 0), ('E', n - T)):
        if side in doors:
            rects += [(u, T, T, a - T), (u, b, T, n - T - b)]
        else:
            rects.append((u, T, T, n - 2 * T))
    return rects


VARIANTS = [('N', '1 door'), ('NS', '2 doors, opposite'), ('NE', '2 doors, corner'),
            ('NES', '3 doors'), ('NESW', '4 doors')]

# 5 ft (1 square wide) hallway walls
H5 = {
    'v': lambda L: [(0, 0, T, L), (1 - T, 0, T, L)],
    'h': lambda L: [(0, 0, L, T), (0, 1 - T, L, T)],
    'corner': [(0, 0, 1, T), (0, T, T, 1 - T), (1 - T, 1 - T, T, T)],
    'tee': [(0, 0, 1, T), (0, 1 - T, T, T), (1 - T, 1 - T, T, T)],
    'cross': [(0, 0, T, T), (1 - T, 0, T, T), (0, 1 - T, T, T), (1 - T, 1 - T, T, T)],
    'dead': [(0, 0, 1, T), (0, T, T, 1 - T), (1 - T, T, T, 1 - T)],
}
V10 = lambda L: [(0, 0, T, L), (2 - T, 0, T, L)]


def room(n, doors, label):
    return (n, n, room_walls(n, doors), f"Room {n}x{n}, {label}")


def hall(w, h, walls, label):
    return (w, h, walls, label)


def strip_right():
    """3 x 10 strip at x = 5: two 10 ft halls and two 5 ft halls, each 5 long."""
    return [(5, 0, hall(2, 5, V10(5), '10 ft hall')), (5, 5, hall(2, 5, V10(5), '10 ft hall')),
            (7, 0, hall(1, 5, H5['v'](5), '5 ft hall')), (7, 5, hall(1, 5, H5['v'](5), '5 ft hall'))]


def small_row(y, x0=0):
    return [(x0 + i, y, hall(1, 1, H5[k], lab)) for i, (k, lab) in
            enumerate([('corner', '5 ft corner'), ('tee', '5 ft T'), ('cross', '5 ft cross'), ('dead', '5 ft dead end')])]


r5 = [room(5, d, l) for d, l in VARIANTS]
r4 = [room(4, d, l) for d, l in VARIANTS]

SHEETS = [
    [(0, 0, r5[0]), (0, 5, r5[1])] + strip_right(),
    [(0, 0, r5[2]), (0, 5, r5[3])] + strip_right(),
    [(0, 0, r5[4]), (0, 5, r4[0]), (4, 5, hall(1, 4, H5['v'](4), '5 ft hall'))]
    + small_row(9) + [(4, 9, hall(1, 1, H5['dead'], '5 ft dead end'))] + strip_right(),
    [(0, 0, r4[1]), (4, 0, r4[2]), (0, 4, r4[3]), (4, 4, r4[4]),
     (0, 8, hall(4, 1, H5['h'](4), '5 ft hall')), (4, 8, hall(4, 1, H5['h'](4), '5 ft hall'))]
    + small_row(9) + [(4, 9, hall(4, 1, H5['h'](4), '5 ft hall'))],
]


def check(sheet):
    occ = set()
    for x, y, (w, h, _, _) in sheet:
        for i in range(int(w)):
            for j in range(int(h)):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    n = len(SHEETS)
    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - Full Rooms.pdf'), pagesize=(PAGE_W * inch, PAGE_H * inch))
    c.setTitle('Dungeon Tiles - Full Rooms')
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - Full Rooms Cut Guide.pdf'), pagesize=(PAGE_W * inch, PAGE_H * inch))
    g.setTitle('Dungeon Tiles - Full Rooms Cut Guide')
    seed = 5000
    for i, sheet in enumerate(SHEETS):
        print(f"sheet {i + 1}: {check(sheet)} of 80 squares used")
        header(c, f"Full Rooms  |  Sheet {i + 1} of {n}")
        for x, y, (w, h, walls, _) in sheet:
            floor(c, x, y, w, h, walls, seed)
            seed += 13
        c.showPage()
        pcs = [(x, y, w, h, lab) for x, y, (w, h, _, lab) in sheet]
        k = cg.draw_guide(g, f"Full Rooms Cut Guide  |  Sheet {i + 1} of {n}", pcs)
        print(f"   {len(pcs)} pieces, {k} cuts")
        g.showPage()
    c.save(); g.save()
