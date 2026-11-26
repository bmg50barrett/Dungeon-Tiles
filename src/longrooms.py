"""Long rooms: 5x6 (25 x 30 ft) and 5x7 (25 x 35 ft), with 5 ft doors for 5 ft hallways.

These are the room sizes Dungeon Maker makes most often after the squares. Every door follows the same rule
as the 4x4 and 5x5 rooms: on each wall it sits k squares in from the wall's left end going clockwise, with
k = (length - 1) // 2. On an odd wall (5 or 7 long) that is the middle; on an even wall (6 long) it is one
square clockwise of the middle, so the doors make a pinwheel. Because the rule reads the same from every
wall, a room tile can be turned any way and still match.

A long room only matches itself when turned end for end, so it takes 9 layouts to cover every room, not 5.
Seen with the room standing tall (the short "end" walls at top and bottom):

    1A  1 door, in an end              2C  2 doors at a corner, end and right side
    1B  1 door, in a side              2D  2 doors at a corner, end and left side
    2A  2 doors, both ends             3A  3 doors, both ends and a side
    2B  2 doors, both sides            3B  3 doors, both sides and an end
                                       4   4 doors

For each size this writes:

    5xN Rooms                      every layout, single-sided (5 sheets, 2 rooms each)
    5xN Rooms Double-Sided         every layout, front and back (3 sheets)
    5xN Room Pack A / B / C        one sheet each: 1 door (end, side); 2 doors (ends, sides); 2 doors (corners)
    5xN Room Pack Double-Sided A   one sheet: 1 door end / both ends, 1 door side / both sides
    5xN Room Pack Double-Sided B   one sheet: 1 door end / corner right, 1 door side / corner left

and a cut guide for each. The rooms are laid sideways, two to a sheet, with 5 ft straights in the spare strip.
The packs follow what tile-mode dungeons need: about 43% of long rooms have 1 door, about 12% each have one of
the four 2-door layouts, and fewer than 6% have 3 or 4."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg
from rooms import H5

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')
SIZES = (6, 7)   # the long side; the short side is always 5

# canonical door sets, with the room standing tall: N and S are the short end walls, E and W the long sides
LAYOUTS = {
    '1A': ('N', '1 door, end'),
    '1B': ('E', '1 door, side'),
    '2A': ('NS', '2 doors, both ends'),
    '2B': ('EW', '2 doors, both sides'),
    '2C': ('NE', '2 doors, corner, right'),
    '2D': ('NW', '2 doors, corner, left'),
    '3A': ('NES', '3 doors, both ends and a side'),
    '3B': ('ESW', '3 doors, both sides and an end'),
    '4': ('NESW', '4 doors'),
}
TURN = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}   # a quarter turn clockwise


def rect_walls(w, h, doors):
    """Walls for a w x h room with a 1-square (5 ft) door on each side in `doors`, placed by the clockwise rule
    above. Each doorway keeps a T-thick wall stub on both sides, like a hallway's own walls. For a 4x4 or 5x5
    room this draws the same doors as the 4x4 Rooms and 5x5 rooms already do."""
    kw, kh = (w - 1) // 2, (h - 1) // 2
    # where each door's square starts, measured from the west end (N, S) or the north end (E, W)
    start = {'N': kw, 'E': kh, 'S': w - 1 - kw, 'W': h - 1 - kh}
    rects = []
    for side, v in (('N', 0), ('S', h - T)):
        if side in doors:
            s = start[side]
            rects += [(0, v, s + T, T), (s + 1 - T, v, w - (s + 1 - T), T)]
        else:
            rects.append((0, v, w, T))
    for side, u in (('W', 0), ('E', w - T)):
        if side in doors:
            s = start[side]
            rects += [(u, T, T, s), (u, s + 1 - T, T, h - T - (s + 1 - T))]
        else:
            rects.append((u, T, T, h - 2 * T))
    return rects


def face_walls(n, code):
    """The canonical face (standing tall: 5 wide, n long)."""
    return rect_walls(5, n, LAYOUTS[code][0])


def sideways_walls(n, code):
    """The same face laid on its side (n wide, 5 tall), as it is drawn on the sheet: a quarter turn clockwise."""
    return rect_walls(n, 5, ''.join(TURN[d] for d in LAYOUTS[code][0]))


def label(n, code):
    return f"Room 5x{n}: {LAYOUTS[code][1]}"


def room(n, front, back=None):
    """A piece: (w, h, front walls, back walls, front label, back label or None)."""
    return (n, 5, sideways_walls(n, front), sideways_walls(n, back or front), label(n, front),
            None if back is None else LAYOUTS[back][1])


def strip(n):
    """5 ft straights (5 long) in the spare strip right of the two rooms: 2 columns beside a 5x6, 1 beside a 5x7."""
    s5 = (1, 5, H5['v'](5), H5['v'](5), '5 ft hall, 5 long', None)
    return [(x, y, s5) for x in range(n, 8) for y in (0, 5)]


def sheet(n, pair_top, pair_bottom):
    """Two rooms, one above the other, each given as (front, back or None)."""
    return [(0, 0, room(n, *pair_top)), (0, 5, room(n, *pair_bottom))] + strip(n)


def editions(n):
    """Every printed file for the 5 x n rooms: (id, name, file, double-sided?, sheets)."""
    single = [[('1A', None), ('1B', None)], [('2A', None), ('2B', None)], [('2C', None), ('2D', None)],
              [('3A', None), ('3B', None)], [('4', None), ('1B', None)]]
    # 12 faces on 6 pieces: common layouts paired with rare ones, and no piece carrying two layouts often needed together
    double = [[('1A', '3A'), ('1B', '3B')], [('1A', '2C'), ('1B', '2D')], [('2A', '4'), ('2B', '1A')]]
    s = lambda pairs: [sheet(n, *p) for p in pairs]
    return [
        (f'rooms-5x{n}', f'5x{n} Rooms, 5 ft Doors', f'5x{n} Rooms', False, s(single)),
        (f'rooms-5x{n}-duplex', f'5x{n} Rooms, 5 ft Doors, Double-Sided', f'5x{n} Rooms Double-Sided', True, s(double)),
        (f'pack-5x{n}-a', f'5x{n} Room Pack A', f'5x{n} Room Pack A', False, s(single[:1])),
        (f'pack-5x{n}-b', f'5x{n} Room Pack B', f'5x{n} Room Pack B', False, s(single[1:2])),
        (f'pack-5x{n}-c', f'5x{n} Room Pack C', f'5x{n} Room Pack C', False, s(single[2:3])),
        (f'pack-5x{n}-duplex-a', f'5x{n} Room Pack, Double-Sided A', f'5x{n} Room Pack Double-Sided A', True,
         s([[('1A', '2A'), ('1B', '2B')]])),
        (f'pack-5x{n}-duplex-b', f'5x{n} Room Pack, Double-Sided B', f'5x{n} Room Pack Double-Sided B', True,
         s([[('1A', '2C'), ('1B', '2D')]])),
    ]


EDITIONS = [e for n in SIZES for e in editions(n)]


def check(items):
    occ = set()
    for x, y, p in items:
        for i in range(int(p[0])):
            for j in range(int(p[1])):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                assert 0 <= x + i < 8 and 0 <= y + j < 10, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    size = (PAGE_W * inch, PAGE_H * inch)
    seed = 21000
    for eid, name, file, two, sheets in EDITIONS:
        n = len(sheets)
        pack = eid.startswith('pack-')
        c = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {file}.pdf"), pagesize=size)
        c.setTitle(f"Dungeon Tiles - {file}")
        g = canvas.Canvas(os.path.join(PDF, f"Dungeon Tiles - {file} Cut Guide.pdf"), pagesize=size)
        g.setTitle(f"Dungeon Tiles - {file} Cut Guide")
        for i, items in enumerate(sheets):
            print(f"{file} sheet {i + 1}: {check(items)} of 80 squares")
            where = 'Print as many as you need' if pack and not two else f"Sheet {i + 1}{'' if two else f' of {n}'}"
            header(c, f"{name}  |  {where}{' FRONT' if two else ''}")
            for x, y, (w, h, fw, bw, _, _) in items:
                floor(c, x, y, w, h, fw, seed); seed += 13
            c.showPage()
            if two:
                header(c, f"{name}  |  Sheet {i + 1} BACK",
                       "Back side. Print duplex, flip on long edge. The ruler must measure exactly 2 inches.")
                for x, y, (w, h, fw, bw, _, _) in items:
                    floor(c, 8 - x - w, y, w, h, bw, seed); seed += 13
                c.showPage()
            lab = lambda f, b: f if b is None else f"{f}  /  back: {b}"
            title = f"{name} Cut Guide" + (f"  |  Sheet {i + 1}" if n > 1 else '') + ('  |  front up' if two else '')
            cg.draw_guide(g, title, [(x, y, w, h, lab(fl, bl)) for x, y, (w, h, _, _, fl, bl) in items])
            g.showPage()
        c.save(); g.save()
