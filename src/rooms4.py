"""4x4 rooms with 5 ft doors, for 5 ft hallways. Writes a single-sided and a
double-sided version, each with a cut guide.

A 5 ft door can't be centered on a 4-square wall, so every door sits one square
in from the left end of its wall, going clockwise around the room (seen from
above, the doors make a pinwheel). With every door following the same rule, the
5 layouts (1 door, 2 opposite, 2 at a corner, 3, 4) cover every room once the
tile is turned, just as they do for the 5x5 rooms."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg
from rooms import H5

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')
N = 4
DOOR_OFFSET = 1   # squares in from the left end of a wall, going clockwise
NAMES = {'N': '1 door', 'NS': '2 doors, opposite', 'NE': '2 doors, corner', 'NES': '3 doors', 'NESW': '4 doors'}


def pinwheel_walls(doors, n=N, k=DOOR_OFFSET):
    """Walls for an n x n room with a 1-square (5 ft) door on each side in `doors`, k squares clockwise from the
    side's left end. Each doorway keeps a T-thick wall stub on both sides, like a hallway's own walls."""
    # where each door's square starts, measured from the west end (N, S) or the north end (E, W)
    start = {'N': k, 'E': k, 'S': n - 1 - k, 'W': n - 1 - k}
    rects = []
    for side, v in (('N', 0), ('S', n - T)):
        if side in doors:
            s = start[side]
            rects += [(0, v, s + T, T), (s + 1 - T, v, n - (s + 1 - T), T)]
        else:
            rects.append((0, v, n, T))
    for side, u in (('W', 0), ('E', n - T)):
        if side in doors:
            s = start[side]
            rects += [(u, T, T, s), (u, s + 1 - T, T, n - T - (s + 1 - T))]
        else:
            rects.append((u, T, T, n - 2 * T))
    return rects


def room(doors):
    return (N, N, pinwheel_walls(doors), f"Room 4x4, {NAMES[doors]} (5 ft)")


def hall(w, h, walls, label):
    return (w, h, walls, label)


def hall_rows(y):
    """An 8 x 2 band of 5 ft hallway pieces: two 4-long straights, then corner, T, crossroads, dead end and a third straight."""
    return ([(0, y, hall(4, 1, H5['h'](4), '5 ft hall')), (4, y, hall(4, 1, H5['h'](4), '5 ft hall'))]
            + [(i, y + 1, hall(1, 1, H5[k], lab)) for i, (k, lab) in
               enumerate([('corner', '5 ft corner'), ('tee', '5 ft T'), ('cross', '5 ft cross'), ('dead', '5 ft dead end')])]
            + [(4, y + 1, hall(4, 1, H5['h'](4), '5 ft hall'))])


# Single-sided: 8 rooms on 2 sheets. The layouts Dungeon Maker uses most (2 doors opposite, 1 door, 2 at a corner) get two copies.
SHEETS = [
    [(0, 0, room('N')), (4, 0, room('NS')), (0, 4, room('NE')), (4, 4, room('NES'))] + hall_rows(8),
    [(0, 0, room('N')), (4, 0, room('NS')), (0, 4, room('NE')), (4, 4, room('NESW'))] + hall_rows(8),
]

# Double-sided: 8 pieces on 2 sheets, a different layout on each face (16 faces: 2 opposite x5, 2 corner x4, 1 door x3, 3 doors x3, 4 doors x1).
PAIRS = [[('NS', 'N'), ('NS', 'NE'), ('NS', 'NES'), ('N', 'NE')],
         [('NS', 'N'), ('NS', 'NE'), ('NES', 'NE'), ('NESW', 'NES')]]


def dhall(w, h, front, back, flab, blab=None):
    return (w, h, front, back, flab, f"back: {blab}" if blab else "same on back")


def dhall_rows(y):
    S4 = lambda: dhall(4, 1, H5['h'](4), H5['h'](4), '5 ft hall')
    CT = dhall(1, 1, H5['corner'], H5['tee'], '5 ft corner', 'T')
    XD = dhall(1, 1, H5['cross'], H5['dead'], '5 ft cross', 'dead end')
    return [(0, y, S4()), (4, y, S4()), (0, y + 1, CT), (1, y + 1, XD), (2, y + 1, CT), (3, y + 1, XD), (4, y + 1, S4())]


DSHEETS = [
    [(x, yy, (N, N, pinwheel_walls(f), pinwheel_walls(b), f"Room 4x4: {NAMES[f]} (5 ft)", f"back: {NAMES[b]}"))
     for (x, yy), (f, b) in zip([(0, 0), (4, 0), (0, 4), (4, 4)], pairs)] + dhall_rows(8)
    for pairs in PAIRS
]


def check(sheet):
    occ = set()
    for x, y, p in sheet:
        for i in range(int(p[0])):
            for j in range(int(p[1])):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    size = (PAGE_W * inch, PAGE_H * inch)
    # single-sided
    n = len(SHEETS)
    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 4x4 Rooms.pdf'), pagesize=size)
    c.setTitle('Dungeon Tiles - 4x4 Rooms')
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 4x4 Rooms Cut Guide.pdf'), pagesize=size)
    g.setTitle('Dungeon Tiles - 4x4 Rooms Cut Guide')
    seed = 9000
    for i, sheet in enumerate(SHEETS):
        print(f"single sheet {i + 1}: {check(sheet)} of 80 squares")
        header(c, f"4x4 Rooms, 5 ft Doors  |  Sheet {i + 1} of {n}")
        for x, y, (w, h, walls, _) in sheet:
            floor(c, x, y, w, h, walls, seed); seed += 13
        c.showPage()
        cg.draw_guide(g, f"4x4 Rooms Cut Guide  |  Sheet {i + 1} of {n}", [(x, y, w, h, lab) for x, y, (w, h, _, lab) in sheet])
        g.showPage()
    c.save(); g.save()
    # double-sided
    n = len(DSHEETS)
    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 4x4 Rooms Double-Sided.pdf'), pagesize=size)
    c.setTitle('Dungeon Tiles - 4x4 Rooms Double-Sided')
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 4x4 Rooms Double-Sided Cut Guide.pdf'), pagesize=size)
    g.setTitle('Dungeon Tiles - 4x4 Rooms Double-Sided Cut Guide')
    for i, sheet in enumerate(DSHEETS):
        print(f"double sheet {i + 1}: {check(sheet)} of 80 squares")
        header(c, f"4x4 Rooms, 5 ft Doors, Double-Sided  |  Sheet {i + 1} FRONT")
        for x, y, (w, h, fw, bw, _, _) in sheet:
            floor(c, x, y, w, h, fw, seed); seed += 13
        c.showPage()
        header(c, f"4x4 Rooms, 5 ft Doors, Double-Sided  |  Sheet {i + 1} BACK",
               "Back side. Print duplex, flip on long edge. The ruler must measure exactly 2 inches.")
        for x, y, (w, h, fw, bw, _, _) in sheet:
            floor(c, 8 - x - w, y, w, h, bw, seed); seed += 13
        c.showPage()
        cg.draw_guide(g, f"Double-Sided 4x4 Rooms Cut Guide  |  Sheet {i + 1}, front up",
                      [(x, y, p[0], p[1], f"{p[4]}  /  {p[5]}") for x, y, p in sheet])
        g.showPage()
    c.save(); g.save()
