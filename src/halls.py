"""5 ft Hallways: a sheet of hallway pieces, single-sided and double-sided, each with a cut guide.

The mix follows what tile-mode dungeons from Dungeon Maker need, about one sheet's worth per average dungeon:
lots of corners, 4-long straights and 1-square straights, a few T-junctions, and the odd 5-long straight,
crossroads and dead end. A longer straight can run under a room tile, or 1 square under a corner, T or
crossroads tile, so the straights don't have to match every length exactly; the 1-square straight covers
the one gap that leaves."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import cut_guide as cg
from rooms import H5

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, '..', 'pdf')

PIECES = {
    'S4': (1, 4, H5['v'](4), '5 ft hall, 4 long'),
    'S5': (5, 1, H5['h'](5), '5 ft hall, 5 long'),
    'S1': (1, 1, H5['v'](1), '5 ft hall, 1 long'),
    'L': (1, 1, H5['corner'], '5 ft corner'),
    'T': (1, 1, H5['tee'], '5 ft T'),
    'X': (1, 1, H5['cross'], '5 ft cross'),
    'D': (1, 1, H5['dead'], '5 ft dead end'),
}


def layout(small):
    """11 upright 4-long straights, one 5-long straight, and the 1x1 pieces `small` (31 of them) in the spaces left."""
    out = [(c, 0, 'S4') for c in range(8)] + [(c, 4, 'S4') for c in range(3)]
    out.append((0, 9, 'S5'))
    spots = [(c, r) for r in range(4, 8) for c in range(3, 8)] + [(c, 8) for c in range(8)] + [(c, 9) for c in range(5, 8)]
    assert len(spots) == len(small) == 31, (len(spots), len(small))
    return out + [(x, y, k) for (x, y), k in zip(spots, small)]


# single-sided: 15 corners, 10 one-square straights, 4 T-junctions, a crossroads and a dead end
SINGLE = layout(['L'] * 15 + ['S1'] * 10 + ['T'] * 4 + ['X', 'D'])

# double-sided: straights are the same on both sides; every small piece has a different back, so one printing can
# lean towards whatever a dungeon needs (31 pieces: corner/1-straight x16, corner/T x8, corner/corner x3, 1-straight/cross x2, 1-straight/dead end x2)
DOUBLE_SMALL = [('L', 'S1')] * 16 + [('L', 'T')] * 8 + [('L', 'L')] * 3 + [('S1', 'X')] * 2 + [('S1', 'D')] * 2
DOUBLE = [(x, y, (k, k)) if k in ('S4', 'S5') else (x, y, None) for x, y, k in layout(['S1'] * 31)]
it = iter(DOUBLE_SMALL)
DOUBLE = [(x, y, faces if faces else next(it)) for x, y, faces in DOUBLE]

SHEETS = [SINGLE]
DSHEETS = [DOUBLE]


def check(items):
    occ = set()
    for x, y, k in items:
        key = k if isinstance(k, str) else k[0]
        w, h = PIECES[key][:2]
        for i in range(w):
            for j in range(h):
                assert (x + i, y + j) not in occ, (x + i, y + j)
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    size = (PAGE_W * inch, PAGE_H * inch)
    seed = 12000
    print(f"single: {check(SINGLE)} of 80 squares, double: {check(DOUBLE)} of 80 squares")

    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 5 ft Hallways.pdf'), pagesize=size)
    c.setTitle('Dungeon Tiles - 5 ft Hallways')
    header(c, '5 ft Hallways  |  Sheet 1 of 1')
    for x, y, k in SINGLE:
        w, h, walls, _ = PIECES[k]
        floor(c, x, y, w, h, walls, seed); seed += 13
    c.showPage(); c.save()
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 5 ft Hallways Cut Guide.pdf'), pagesize=size)
    g.setTitle('Dungeon Tiles - 5 ft Hallways Cut Guide')
    cg.draw_guide(g, '5 ft Hallways Cut Guide  |  Sheet 1 of 1',
                  [(x, y, PIECES[k][0], PIECES[k][1], PIECES[k][3].replace('5 ft ', '')) for x, y, k in SINGLE])
    g.showPage(); g.save()

    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 5 ft Hallways Double-Sided.pdf'), pagesize=size)
    c.setTitle('Dungeon Tiles - 5 ft Hallways Double-Sided')
    header(c, '5 ft Hallways, Double-Sided  |  Sheet 1 FRONT')
    for x, y, (f, b) in DOUBLE:
        w, h, walls, _ = PIECES[f]
        floor(c, x, y, w, h, walls, seed); seed += 13
    c.showPage()
    header(c, '5 ft Hallways, Double-Sided  |  Sheet 1 BACK',
           'Back side. Print duplex, flip on long edge. The ruler must measure exactly 2 inches.')
    for x, y, (f, b) in DOUBLE:
        w, h, walls, _ = PIECES[b]
        floor(c, 8 - x - w, y, w, h, walls, seed); seed += 13
    c.showPage(); c.save()
    short = {'S4': '4 long', 'S5': '5 long', 'S1': '1 long', 'L': 'corner', 'T': 'T', 'X': 'cross', 'D': 'dead end'}
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - 5 ft Hallways Double-Sided Cut Guide.pdf'), pagesize=size)
    g.setTitle('Dungeon Tiles - 5 ft Hallways Double-Sided Cut Guide')
    cg.draw_guide(g, 'Double-Sided 5 ft Hallways Cut Guide  |  Sheet 1, front up',
                  [(x, y, PIECES[f][0], PIECES[f][1], short[f] if f == b else f"{short[f]}  /  back: {short[b]}") for x, y, (f, b) in DOUBLE])
    g.showPage(); g.save()
