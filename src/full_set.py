import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import *

# ---- piece definitions: (name, w, h, draw(c, x, y, seed))
def fl(walls, w=2, h=2, cracks=True):
    return lambda c, x, y, s: floor(c, x, y, w, h, walls, s, cracks)

W = {
    'straight': [(0, 0, T, 2), (2 - T, 0, T, 2)],
    'straight4': [(0, 0, T, 4), (2 - T, 0, T, 4)],
    'corner': [(0, 0, 2, T), (0, T, T, 2 - T), (2 - T, 2 - T, T, T)],
    'tee': [(0, 0, 2, T), (0, 2 - T, T, T), (2 - T, 2 - T, T, T)],
    'cross': [(0, 0, T, T), (2 - T, 0, T, T), (0, 2 - T, T, T), (2 - T, 2 - T, T, T)],
    'dead': [(0, 0, 2, T), (0, T, T, 2 - T), (2 - T, T, T, 2 - T)],
    'outer': [(0, 0, 2, T), (0, T, T, 2 - T)],
    'edge': [(0, 0, 2, T)],
    'edge4': [(0, 0, T, 4)],
    'inner': [(2 - T, 2 - T, T, T)],
}

big, tall, small, minis, doors = [], [], [], [], []
def add(lst, n, *item):
    lst.extend([item] * n)

add(big, 4, 'floor4x4', lambda c, x, y, s: floor(c, x, y, 4, 4, [], s))
add(tall, 6, 'corridor2x4', fl(W['straight4'], 2, 4))
add(tall, 6, 'edge2x4', fl(W['edge4'], 2, 4))
add(tall, 4, 'floor2x4', fl([], 2, 4))
add(tall, 2, 'stairs', lambda c, x, y, s: stairs(c, x, y, s))
add(small, 4, 'straight', fl(W['straight']))
add(small, 4, 'corner', fl(W['corner']))
add(small, 3, 'tee', fl(W['tee']))
add(small, 2, 'cross', fl(W['cross']))
add(small, 2, 'dead', fl(W['dead']))
add(small, 8, 'outer', fl(W['outer']))
add(small, 8, 'edge', fl(W['edge']))
add(small, 4, 'inner', fl(W['inner']))
add(small, 6, 'floor2x2', fl([]))
add(small, 1, 'spikepit', lambda c, x, y, s: pit(c, x, y, s, spikes=True))
add(small, 1, 'pit', lambda c, x, y, s: pit(c, x, y, s))
add(small, 2, 'collapsed', lambda c, x, y, s: collapsed(c, x, y, s))
add(minis, 2, 'pit1', lambda c, x, y, s: pit(c, x, y, s, w=1, h=1))
add(minis, 2, 'ladder', lambda c, x, y, s: ladder(c, x, y, s))
add(minis, 2, 'trapdoor', lambda c, x, y, s: trapdoor(c, x, y, s))
add(minis, 2, 'spiral', lambda c, x, y, s: spiral(c, x, y, s))
for k, n in [('wood', 7), ('locked', 3), ('iron', 2), ('portcullis', 2), ('secret', 4),
             ('broken', 2), ('arch', 2), ('sealed', 2)]:
    doors += [k] * n

# group minis and doors into 2x2 blocks
def mini_block(items):
    def draw(c, x, y, s):
        for i, (_, f) in enumerate(items):
            f(c, x + i % 2, y + i // 2, s + i)
    return draw

def door_block(kinds):
    def draw(c, x, y, s):
        for i, k in enumerate(kinds):
            door(c, x, y + i * 0.5, k, s + i)
    return draw

for i in range(0, len(minis), 4):
    small.append(('minis', mini_block(minis[i:i + 4])))
for i in range(0, len(doors), 4):
    small.append(('doors', door_block(doors[i:i + 4])))

# ---- pack onto pages: 4 x 5 grid of 2x2 cells
COLS, ROWS = 4, 5
pages = []

def place(cw, ch):
    for p in pages:
        for r in range(ROWS - ch + 1):
            for col in range(COLS - cw + 1):
                if all(not p[rr][cc] for rr in range(r, r + ch) for cc in range(col, col + cw)):
                    for rr in range(r, r + ch):
                        for cc in range(col, col + cw):
                            p[rr][cc] = True
                    return pages.index(p), col, r
    pages.append([[False] * COLS for _ in range(ROWS)])
    return place(cw, ch)

placed = []
for item in big:
    placed.append((*place(2, 2), item))
for item in tall:
    placed.append((*place(1, 2), item))
for item in small:
    placed.append((*place(1, 1), item))

# fill leftover cells with extra plain floors and room edges
extra = 0
for pi, p in enumerate(pages):
    for r in range(ROWS):
        for col in range(COLS):
            if not p[r][col]:
                p[r][col] = True
                item = ('floor2x2', fl([])) if extra % 2 == 0 else ('edge', fl(W['edge']))
                placed.append((pi, col, r, item))
                extra += 1

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdf', 'Dungeon Tiles - Full Set.pdf')
c = canvas.Canvas(out, pagesize=(PAGE_W * inch, PAGE_H * inch))
c.setTitle('Dungeon Tiles - Full Set')
seed = 1000
counts = {}
for pi in range(len(pages)):
    header(c, f"Sheet {pi + 1} of {len(pages)}")
    for (pj, col, r, (name, f)) in placed:
        if pj == pi:
            f(c, col * 2, r * 2, seed)
            seed += 17
            counts[name] = counts.get(name, 0) + 1
    c.showPage()
c.save()
print(len(pages), 'pages; extras', extra)
print(counts)
