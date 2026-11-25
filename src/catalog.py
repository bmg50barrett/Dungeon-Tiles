"""Build catalog/tiles.json: every tile design (face) and every physical piece
in the printed files, so other tools (like a dungeon generator's bill of
materials) can work out which pieces a map needs.

Each piece's size and openings are worked out from the same wall definitions
that draw the sheets, so the catalog can't drift from what is printed.

Edge convention: sides are listed N, E, S, W with the face in its canonical
orientation. Openings on a side are [offset, width] in grid squares, with
offsets measured clockwise around the piece: N from its west end, E from its
north end, S from its east end, W from its south end. With that convention,
turning a face 90 degrees clockwise just moves each side's openings to the
next side (N to E, E to S, S to W, W to N) and swaps width and height."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineart import T
import rooms, rooms_duplex

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'catalog', 'tiles.json')
CATALOG_VERSION = 1
EPS = 1e-6
SIDES = ['N', 'E', 'S', 'W']

# ---------------------------------------------------------------- faces
# Stable IDs. Never reuse or renumber an ID once published; add new ones.
DOORS = [('1', 'N', '1 door'), ('2O', 'NS', '2 doors, opposite'), ('2C', 'NE', '2 doors, corner'),
         ('3', 'NES', '3 doors'), ('4', 'NESW', '4 doors')]
FACES = {}
for n, ft, dw in ((4, 20, 10), (5, 25, 5)):
    for suffix, doors, label in DOORS:
        FACES[f"R{n}-{suffix}"] = dict(name=f"Room {n}x{n} ({ft} ft), {label}", kind='room',
                                       door_width_ft=dw, w=n, h=n, walls=rooms.room_walls(n, doors))
for L in (4, 5):
    FACES[f"H5-S{L}"] = dict(name=f"5 ft hall, straight, {L} long ({L * 5} ft)", kind='hall', hall_width_ft=5,
                             w=1, h=L, walls=rooms.H5['v'](L))
FACES["H10-S5"] = dict(name="10 ft hall, straight, 5 long (25 ft)", kind='hall', hall_width_ft=10,
                       w=2, h=5, walls=rooms.V10(5))
for fid, key, label in (('H5-L', 'corner', 'corner'), ('H5-T', 'tee', 'T-junction'),
                        ('H5-X', 'cross', 'crossroads'), ('H5-D', 'dead', 'dead end')):
    FACES[fid] = dict(name=f"5 ft hall, {label}", kind='hall', hall_width_ft=5, w=1, h=1, walls=rooms.H5[key])


# ---------------------------------------------------------------- geometry
def signature(w, h, walls):
    """Openings per side, snapped to whole grid squares."""
    def uncovered(L, spans):
        out, cur = [], 0.0
        for a, b in sorted(spans):
            if a > cur + EPS:
                out.append((cur, a))
            cur = max(cur, b)
        if cur < L - EPS:
            out.append((cur, L))
        return [[math.floor(a + 0.3), math.ceil(b - 0.3) - math.floor(a + 0.3)] for a, b in out]

    n = [(x, x + rw) for x, y, rw, rh in walls if y <= EPS]
    e = [(y, y + rh) for x, y, rw, rh in walls if x + rw >= w - EPS]
    s = [(w - (x + rw), w - x) for x, y, rw, rh in walls if y + rh >= h - EPS]
    wst = [(h - (y + rh), h - y) for x, y, rw, rh in walls if x <= EPS]
    return (w, h, tuple(tuple(map(tuple, uncovered(L, sp))) for L, sp in
                        ((w, n), (h, e), (w, s), (h, wst))))


def rotate_cw(sig):
    w, h, (n, e, s, wst) = sig
    return (h, w, (wst, n, e, s))


SIGS = {fid: signature(f['w'], f['h'], f['walls']) for fid, f in FACES.items()}


def identify(w, h, walls):
    """Return (face id, quarter turns clockwise from the canonical face to how it is drawn)."""
    sig = signature(w, h, walls)
    for fid, fsig in SIGS.items():
        r = fsig
        for turns in range(4):
            if r == sig:
                return fid, turns
            r = rotate_cw(r)
    raise ValueError(f"no catalog face matches a {w}x{h} piece with openings {sig[2]}")


# ---------------------------------------------------------------- editions
def single_sided():
    pieces = []
    for si, sheet in enumerate(rooms.SHEETS, 1):
        for x, y, (w, h, walls, _) in sheet:
            fid, _ = identify(w, h, walls)
            pieces.append(dict(faces=[fid], sheet=si, at=[x, y]))
    return dict(id='full-rooms', name='Full Rooms', file='pdf/Dungeon Tiles - Full Rooms.pdf',
                cut_guide='pdf/Dungeon Tiles - Full Rooms Cut Guide.pdf', double_sided=False,
                sheets=len(rooms.SHEETS), pieces=pieces)


def double_sided():
    pieces = []
    for si, sheet in enumerate(rooms_duplex.SHEETS, 1):
        for x, y, (w, h, fw, bw, _, _) in sheet:
            front, _ = identify(w, h, fw)
            back, _ = identify(w, h, bw)
            pieces.append(dict(faces=[front, back], sheet=si, at=[x, y]))
    return dict(id='full-rooms-duplex', name='Full Rooms, Double-Sided',
                file='pdf/Dungeon Tiles - Full Rooms Double-Sided.pdf',
                cut_guide='pdf/Dungeon Tiles - Full Rooms Double-Sided Cut Guide.pdf', double_sided=True,
                sheets=len(rooms_duplex.SHEETS), pieces=pieces)


def face_counts(ed):
    counts = {}
    for p in ed['pieces']:
        for f in set(p['faces']):
            counts[f] = counts.get(f, 0) + 1
    return dict(sorted(counts.items()))


if __name__ == '__main__':
    editions = [single_sided(), double_sided()]
    for ed in editions:
        ed['faces_available'] = face_counts(ed)
    faces = {}
    for fid, f in FACES.items():
        _, _, sides = SIGS[fid]
        entry = {'name': f['name'], 'kind': f['kind'], 'size': [f['w'], f['h']]}
        for k in ('door_width_ft', 'hall_width_ft'):
            if k in f:
                entry[k] = f[k]
        entry['openings'] = {s: [list(o) for o in sides[i]] for i, s in enumerate(SIDES)}
        faces[fid] = entry
    used = {f for ed in editions for p in ed['pieces'] for f in p['faces']}
    unused = sorted(set(FACES) - used)
    catalog = {
        'catalog_version': CATALOG_VERSION,
        'grid': {'square_inches': 1, 'square_feet': 5},
        'wall_thickness_inches': T,
        'edge_convention': ('Sides N, E, S, W in the canonical orientation. Openings are [offset, width] in '
                            'squares, offsets measured clockwise: N from the west end, E from the north end, '
                            'S from the east end, W from the south end. A face can be turned to any of 4 '
                            'orientations; turning 90 degrees clockwise moves openings N->E->S->W->N.'),
        'faces': faces,
        'editions': editions,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump(catalog, fh, indent=2)
        fh.write('\n')
    print(f"{len(faces)} faces, unused: {unused or 'none'}")
    for ed in editions:
        print(f"{ed['id']}: {len(ed['pieces'])} pieces on {ed['sheets']} sheets -> {ed['faces_available']}")
