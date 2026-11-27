"""Doorless rooms: plain walled rooms in 10 sizes, for use with standing door markers.

Instead of printing a tile for every door layout, these rooms have a solid wall all the way round. Doors are
shown with door markers (such as the C4Labs ones: a 1 inch door on a round base) stood on the wall line where
a hallway or another room meets it. One design per size covers every room of that size, so 10 designs do the
work that would take 5 to 9 door layouts per size with printed doors.

Sizes (in squares; 1 square = 5 ft): 4x4, 4x5, 4x6, 4x7, 4x8, 5x5, 5x6, 5x7, 5x8, 6x6. These cover the
room sizes Dungeon Maker makes most often.

This writes one sheet per size (as many of that room as fit, with 5 ft hallway straights in the spare space),
each as its own file, plus one file with all ten sheets, and a cut guide for each. There are no double-sided
versions: a piece can only carry the same size on its back, and every room of a size is the same."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg
from rooms import H5
from longrooms import rect_walls

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')
SIZES = ['4x4', '4x5', '4x6', '4x7', '4x8', '5x5', '5x6', '5x7', '5x8', '6x6']


def room(w, h):
    """A doorless room w across and h down."""
    a, b = sorted((w, h))
    return (w, h, rect_walls(w, h, ''), f"Room {a}x{b}, no doors")


def s(L, vertical=True):
    """A 5 ft straight, L long."""
    return (1, L, H5['v'](L), f'5 ft hall, {L} long') if vertical else (L, 1, H5['h'](L), f'5 ft hall, {L} long')


def col(x, y, lengths):
    """Vertical straights stacked down one column."""
    out = []
    for L in lengths:
        out.append((x, y, s(L)))
        y += L
    return out


def row(x, y, lengths):
    out = []
    for L in lengths:
        out.append((x, y, s(L, False)))
        x += L
    return out


# each sheet is 8 squares across and 10 down
SHEETS = {
    '4x4': [(0, 0, room(4, 4)), (4, 0, room(4, 4)), (0, 4, room(4, 4)), (4, 4, room(4, 4))]
           + row(0, 8, [4, 4]) + row(0, 9, [4, 4]),
    '4x5': [(0, 0, room(4, 5)), (4, 0, room(4, 5)), (0, 5, room(4, 5)), (4, 5, room(4, 5))],
    '4x6': [(0, 0, room(4, 6)), (4, 0, room(4, 6)), (0, 6, room(6, 4))] + col(6, 6, [4]) + col(7, 6, [4]),
    '4x7': [(0, 0, room(4, 7)), (4, 0, room(4, 7))] + row(0, 7, [4, 4]) + row(0, 8, [4, 4]) + row(0, 9, [4, 4]),
    '4x8': [(0, 0, room(4, 8)), (4, 0, room(4, 8))] + row(0, 8, [4, 4]) + row(0, 9, [4, 4]),
    '5x5': [(0, 0, room(5, 5)), (0, 5, room(5, 5))] + col(5, 0, [5, 5]) + col(6, 0, [5, 5]) + col(7, 0, [5, 5]),
    '5x6': [(0, 0, room(6, 5)), (0, 5, room(6, 5))] + col(6, 0, [5, 5]) + col(7, 0, [5, 5]),
    '5x7': [(0, 0, room(7, 5)), (0, 5, room(7, 5))] + col(7, 0, [5, 5]),
    '5x8': [(0, 0, room(8, 5)), (0, 5, room(8, 5))],
    # one 6x6 fills most of a sheet, so the space below it takes two 4x4s
    '6x6': [(0, 0, room(6, 6)), (0, 6, room(4, 4)), (4, 6, room(4, 4))] + col(6, 0, [5, 1]) + col(7, 0, [5, 1]),
}

# (id, name, file, sheets): one file per size, and one with them all
EDITIONS = [(f'doorless-{z}', f'{z} Doorless Rooms', f'{z} Doorless Rooms', [z]) for z in SIZES] + \
           [('doorless-all', 'Doorless Rooms, All Sizes', 'Doorless Rooms All Sizes', SIZES)]


def check(items):
    occ = set()
    for x, y, p in items:
        for i in range(p[0]):
            for j in range(p[1]):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                assert 0 <= x + i < 8 and 0 <= y + j < 10, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    size = (PAGE_W * inch, PAGE_H * inch)
    for z in SIZES:
        print(f"{z}: {sum(1 for _, _, p in SHEETS[z] if p[3].startswith('Room'))} rooms, {check(SHEETS[z])} of 80 squares used")
    for eid, name, file, sizes in EDITIONS:
        seed = 31000
        c = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {file}.pdf"), pagesize=size)
        c.setTitle(f"Dungeon Tiles - {file}")
        g = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {file} Cut Guide.pdf"), pagesize=size)
        g.setTitle(f"Dungeon Tiles - {file} Cut Guide")
        for i, z in enumerate(sizes):
            where = 'Print as many as you need' if len(sizes) == 1 else f'Sheet {i + 1} of {len(sizes)}: {z}'
            header(c, f"{name}  |  {where}", "Use door markers for the doors. The ruler must measure exactly 2 inches.")
            for x, y, (w, h, walls, _) in SHEETS[z]:
                floor(c, x, y, w, h, walls, seed); seed += 13
            c.showPage()
            cg.draw_guide(g, f"{name} Cut Guide" + (f"  |  Sheet {i + 1}: {z}" if len(sizes) > 1 else ''),
                          [(x, y, w, h, lab) for x, y, (w, h, _, lab) in SHEETS[z]])
            g.showPage()
        c.save(); g.save()
