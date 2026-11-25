"""Double-sided Full Rooms. Each piece has a front and a back face of the same
size. Pages come in front/back pairs, with each back page mirrored left to right
so it lines up when the sheet is printed duplex, flipped on the long edge."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *
import lineart
import cut_guide as cg
from rooms import room_walls, H5, V10

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdf')
NAMES = {'N': '1 door', 'NS': '2 doors, opposite', 'NE': '2 doors, corner', 'NES': '3 doors', 'NESW': '4 doors'}


def rm(n, front, back):
    return (n, n, room_walls(n, front), room_walls(n, back),
            f"Room {n}x{n}: {NAMES[front]}", f"back: {NAMES[back]}")


def hl(w, h, front, back, flab, blab=None):
    return (w, h, front, back, flab, f"back: {blab}" if blab else "same on back")


V5 = lambda L: hl(1, L, H5['v'](L), H5['v'](L), '5 ft hall')
H5L = lambda L: hl(L, 1, H5['h'](L), H5['h'](L), '5 ft hall')
V10L = lambda L: hl(2, L, V10(L), V10(L), '10 ft hall')
CT = hl(1, 1, H5['corner'], H5['tee'], '5 ft corner', 'T')
XD = hl(1, 1, H5['cross'], H5['dead'], '5 ft cross', 'dead end')

strip = [(5, 0, V10L(5)), (5, 5, V10L(5)), (7, 0, V5(5)), (7, 5, V5(5))]

SHEETS = [
    # 5x5 rooms
    [(0, 0, rm(5, 'N', 'NS')), (0, 5, rm(5, 'NE', 'NES'))] + strip,
    # last 5x5 plus two 4x4s
    [(0, 0, rm(5, 'NESW', 'N')), (0, 5, rm(4, 'N', 'NS')), (4, 5, hl(1, 4, H5['v'](4), H5['v'](4), '5 ft hall')),
     (0, 9, CT), (1, 9, XD), (2, 9, CT), (3, 9, XD), (4, 9, CT)] + strip,
    # four more 4x4s and hallways
    [(0, 0, rm(4, 'NE', 'NES')), (4, 0, rm(4, 'NESW', 'N')), (0, 4, rm(4, 'N', 'NE')), (4, 4, rm(4, 'NS', 'NES')),
     (0, 8, H5L(4)), (4, 8, H5L(4)), (0, 9, XD), (1, 9, CT), (2, 9, XD), (3, 9, CT), (4, 9, H5L(4))],
]


def check(sheet):
    occ = set()
    for x, y, p in sheet:
        for i in range(int(p[0])):
            for j in range(int(p[1])):
                assert (x + i, y + j) not in occ
                occ.add((x + i, y + j))
    return len(occ)


if __name__ == '__main__':
    n = len(SHEETS)
    c = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - Full Rooms Double-Sided.pdf'),
                      pagesize=(PAGE_W * inch, PAGE_H * inch))
    c.setTitle('Dungeon Tiles - Full Rooms Double-Sided')
    g = canvas.Canvas(os.path.join(PDF, 'Dungeon Tiles - Full Rooms Double-Sided Cut Guide.pdf'),
                      pagesize=(PAGE_W * inch, PAGE_H * inch))
    g.setTitle('Dungeon Tiles - Full Rooms Double-Sided Cut Guide')
    seed = 7000
    for i, sheet in enumerate(SHEETS):
        print(f"sheet {i + 1}: {check(sheet)} of 80 squares")
        # front
        header(c, f"Full Rooms, Double-Sided  |  Sheet {i + 1} FRONT")
        for x, y, (w, h, fw, bw, _, _) in sheet:
            floor(c, x, y, w, h, fw, seed); seed += 13
        c.showPage()
        # back: mirrored left to right for a long-edge flip
        header(c, f"Full Rooms, Double-Sided  |  Sheet {i + 1} BACK",
               "Back side. Print duplex, flip on long edge. The ruler must measure exactly 2 inches.")
        for x, y, (w, h, fw, bw, _, _) in sheet:
            floor(c, 8 - x - w, y, w, h, bw, seed); seed += 13
        c.showPage()
        pcs = [(x, y, p[0], p[1], f"{p[4]}  /  {p[5]}") for x, y, p in sheet]
        k = cg.draw_guide(g, f"Double-Sided Rooms Cut Guide  |  Sheet {i + 1}, front up", pcs)
        print(f"   {len(pcs)} pieces, {k} cuts")
        g.showPage()
    c.save(); g.save()
