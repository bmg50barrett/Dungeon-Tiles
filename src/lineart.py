"""Line-art dungeon tiles, vector, for printing on gray cardstock.
1 square = 1 inch = 5 ft. Floors are left unprinted (paper color)."""
import math, os, random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

PAGE_W, PAGE_H = 8.5, 11
OX, OY = 0.25, 0.75        # tile area top-left on the page, inches
T = 0.15                   # wall thickness, inches
INK = (0, 0, 0)
GRID = 0.45                # grid gray level
HATCH_GAP = 0.045


class Tile:
    """Drawing context for one tile; coordinates in squares from the tile's top-left."""
    def __init__(self, c, x, y, w, h, seed):
        self.c, self.x, self.y, self.w, self.h = c, x, y, w, h
        self.rng = random.Random(seed)

    def P(self, u, v):
        return ((OX + self.x + u) * inch, (PAGE_H - OY - self.y - v) * inch)

    # ---- primitives
    def path(self, pts, close=True):
        p = self.c.beginPath()
        p.moveTo(*self.P(*pts[0]))
        for q in pts[1:]:
            p.lineTo(*self.P(*q))
        if close:
            p.close()
        return p

    def rect_pts(self, u, v, w, h):
        return [(u, v), (u + w, v), (u + w, v + h), (u, v + h)]

    def line(self, a, b, width=1.0, gray=0.0, dash=None):
        c = self.c
        c.setStrokeGray(gray); c.setLineWidth(width)
        c.setDash(dash or [])
        c.line(*self.P(*a), *self.P(*b))
        c.setDash([])

    def hatch(self, pts, gap=HATCH_GAP, angle=45, width=0.5, cross=False):
        c = self.c
        c.saveState()
        c.clipPath(self.path(pts), stroke=0, fill=0)
        c.setStrokeGray(0); c.setLineWidth(width)
        xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        r = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 0.1
        for ang in ([angle, angle + 90] if cross else [angle]):
            a = math.radians(ang)
            dx, dy = math.cos(a), math.sin(a)
            n = int(r / gap) + 1
            for i in range(-n, n + 1):
                ox, oy = cx - dy * i * gap, cy + dx * i * gap
                c.line(*self.P(ox - dx * r, oy - dy * r), *self.P(ox + dx * r, oy + dy * r))
        c.restoreState()

    def fill(self, pts, gray=0.0, stroke=None, width=1.0):
        c = self.c
        c.setFillGray(gray)
        if stroke is not None:
            c.setStrokeGray(stroke); c.setLineWidth(width)
        c.drawPath(self.path(pts), stroke=1 if stroke is not None else 0, fill=1)

    def outline(self, pts, width=1.0, gray=0.0, close=True):
        c = self.c
        c.setStrokeGray(gray); c.setLineWidth(width)
        c.drawPath(self.path(pts, close), stroke=1, fill=0)

    # ---- tile features
    def grid(self):
        for i in range(1, int(self.w)):
            self.line((i, 0), (i, self.h), 0.45, GRID)
        for j in range(1, int(self.h)):
            self.line((0, j), (self.w, j), 0.45, GRID)

    def cracks(self, n=None):
        n = n if n is not None else self.rng.randint(1, 2) * max(1, int(self.w * self.h / 4))
        for _ in range(n):
            u = self.rng.uniform(0.35, self.w - 0.35); v = self.rng.uniform(0.35, self.h - 0.35)
            ang = self.rng.uniform(0, 2 * math.pi)
            pts = [(u, v)]
            for _ in range(self.rng.randint(2, 4)):
                ang += self.rng.gauss(0, 0.7)
                u += math.cos(ang) * 0.07; v += math.sin(ang) * 0.07
                pts.append((u, v))
            self.outline(pts, 0.5, 0.25, close=False)
        for _ in range(n):
            u = self.rng.uniform(0.3, self.w - 0.3); v = self.rng.uniform(0.3, self.h - 0.3)
            s = 0.018
            self.outline([(u - s, v), (u, v - s), (u + s, v + s * 0.4)], 0.5, 0.25)

    def walls(self, rects):
        """Hatched rock with a bold line on every edge that faces floor (not the tile edge)."""
        eps = 1e-6
        for (u, v, w, h) in rects:
            pts = self.rect_pts(u, v, w, h)
            self.hatch(pts, gap=0.04, angle=45, width=0.55)
        # bold floor-facing edges
        for (u, v, w, h) in rects:
            edges = [((u, v), (u + w, v)), ((u + w, v), (u + w, v + h)),
                     ((u, v + h), (u + w, v + h)), ((u, v), (u, v + h))]
            for a, b in edges:
                on_border = ((abs(a[0] - b[0]) < eps and (abs(a[0]) < eps or abs(a[0] - self.w) < eps)) or
                             (abs(a[1] - b[1]) < eps and (abs(a[1]) < eps or abs(a[1] - self.h) < eps)))
                if on_border:
                    continue
                # skip parts of the edge covered by another wall rect
                segs = self._uncovered(a, b, rects, (u, v, w, h))
                for s0, s1 in segs:
                    self.line(s0, s1, 2.2, 0)

    def _uncovered(self, a, b, rects, me):
        horiz = abs(a[1] - b[1]) < 1e-6
        lo, hi = (min(a[0], b[0]), max(a[0], b[0])) if horiz else (min(a[1], b[1]), max(a[1], b[1]))
        fixed = a[1] if horiz else a[0]
        cover = []
        for r in rects:
            if r == me:
                continue
            u, v, w, h = r
            if horiz and v - 1e-6 <= fixed <= v + h + 1e-6 and not (abs(fixed - v) < 1e-6 or abs(fixed - v - h) < 1e-6):
                cover.append((u, u + w))
            elif horiz and (abs(fixed - v) < 1e-6 or abs(fixed - v - h) < 1e-6):
                # touching neighbour on the other side of this edge: edge is interior, hide it
                cover.append((u, u + w))
            elif not horiz and (u - 1e-6 <= fixed <= u + w + 1e-6):
                cover.append((v, v + h))
        segs, cur = [], lo
        for c0, c1 in sorted(cover):
            if c1 <= cur or c0 >= hi:
                continue
            if c0 > cur:
                segs.append((cur, c0))
            cur = max(cur, c1)
        if cur < hi:
            segs.append((cur, hi))
        return [((s, fixed), (e, fixed)) if horiz else ((fixed, s), (fixed, e)) for s, e in segs if e - s > 1e-4]

    def cut_line(self):
        self.outline(self.rect_pts(0, 0, self.w, self.h), 0.35, 0.55)


# ======================================================================= tiles
def floor(c, x, y, w, h, walls, seed, cracks=True):
    t = Tile(c, x, y, w, h, seed)
    t.grid()
    if cracks:
        t.cracks()
    t.walls(walls)
    t.cut_line()


def stairs(c, x, y, seed, w=2, h=4):
    """Step lines close together at the low end. Reads either way round."""
    t = Tile(c, x, y, w, h, seed)
    top = 0.5
    t.grid()
    n = 14
    v = top
    gaps = [0.34 - 0.012 * i for i in range(n)]
    scale = (h - top) / sum(gaps)
    for i, g in enumerate(gaps):
        t.line((T, v), (w - T, v), 1.1 if i else 1.6, 0)
        v += g * scale
    t.walls([(0, 0, T, h), (w - T, 0, T, h)])
    t.cut_line()


def pit(c, x, y, seed, w=2, h=2, spikes=False):
    t = Tile(c, x, y, w, h, seed)
    t.grid()
    m = 0.16 if w >= 2 else 0.18
    o = t.rect_pts(m, m, w - 2 * m, h - 2 * m)
    d = 0.32 * min(w, h) / 2
    i = t.rect_pts(m + d, m + d, w - 2 * (m + d), h - 2 * (m + d))
    t.hatch(i, gap=0.035, cross=True, width=0.5)
    # shaft walls in perspective
    for k in range(4):
        side = [o[k], o[(k + 1) % 4], i[(k + 1) % 4], i[k]]
        t.hatch(side, gap=0.07 if k in (0, 3) else 0.05, angle=[0, 90, 0, 90][k] + 15, width=0.45)
        t.outline(side, 0.6)
    t.outline(o, 2.2)
    if spikes:
        # top-down spikes: evenly spaced staggered rows of small circles
        x0, x1 = m + d, w - m - d
        y0, y1 = m + d, h - m - d
        n = 5
        step = (x1 - x0) / n
        r = 0.045
        for row in range(n):
            v = y0 + step * (row + 0.5)
            cols = n if row % 2 == 0 else n - 1
            off = 0.5 if row % 2 == 0 else 1.0
            for k in range(cols):
                u = x0 + step * (k + off)
                px, py = t.P(u, v)
                c.setFillGray(1); c.setStrokeGray(0); c.setLineWidth(1.0)
                c.circle(px, py, r * inch, fill=1, stroke=1)
                c.setFillGray(0)
                c.circle(px, py, 0.012 * inch, fill=1, stroke=0)
    t.cut_line()


def collapsed(c, x, y, seed, w=2, h=2):
    t = Tile(c, x, y, w, h, seed)
    t.grid()
    cx, cy = w / 2, h / 2
    pts = []
    N = 22
    for k in range(N):
        a = 2 * math.pi * k / N
        r = 0.55 * (1 + t.rng.uniform(-0.28, 0.28))
        pts.append((cx + math.cos(a) * r * w / 2 / 1.0, cy + math.sin(a) * r * h / 2))
    t.fill(pts, gray=1.0)                       # knock out grid inside the hole (white)
    t.hatch(pts, gap=0.035, cross=True, width=0.5)
    t.outline(pts, 2.0)
    for _ in range(24):
        a = t.rng.uniform(0, 2 * math.pi)
        r = 0.55 * w / 2 * t.rng.uniform(1.08, 1.5)
        u, v = cx + math.cos(a) * r, cy + math.sin(a) * r
        if not (0.08 < u < w - 0.08 and 0.08 < v < h - 0.08):
            continue
        s = t.rng.uniform(0.03, 0.08)
        rock = [(u + s * math.cos(b) * t.rng.uniform(0.6, 1.2), v + s * math.sin(b) * t.rng.uniform(0.6, 1.2))
                for b in sorted(t.rng.uniform(0, 2 * math.pi) for _ in range(6))]
        t.outline(rock, 0.8)
    t.cut_line()


# ---- overlays
def door(c, x, y, kind, seed):
    """2 x 0.5 overlay laid across a 10 ft opening, centred on the joint between tiles."""
    t = Tile(c, x, y, 2, 0.5, seed)
    w, h = 2, 0.5
    L, R, M = T, w - T, 1.0
    a, b = 0.17, 0.33
    if kind in ('secret', 'sealed'):
        t.walls([(0, 0, T, h), (w - T, 0, T, h), (T, 0.15, w - 2 * T, 0.2)])
    else:
        t.walls([(0, 0, T, h), (w - T, 0, T, h)])
    if kind in ('wood', 'locked'):
        for x0, x1 in ((L, M), (M, R)):
            t.outline(t.rect_pts(x0, a, x1 - x0, b - a), 1.4)
            for k in range(1, 7):
                xx = x0 + (x1 - x0) * k / 7
                t.line((xx, a), (xx, b), 0.5, 0.3)
        for xx in (L + 0.1, M - 0.13, M + 0.13, R - 0.1):
            t.fill(t.rect_pts(xx - 0.02, a - 0.015, 0.04, b - a + 0.03), gray=0)
        if kind == 'locked':
            t.fill(t.rect_pts(M - 0.06, a + 0.01, 0.12, b - a - 0.02), gray=1, stroke=0, width=1)
            t.fill([(M - 0.012, a + 0.03), (M + 0.012, a + 0.03), (M + 0.012, b - 0.03), (M - 0.012, b - 0.03)], gray=0)
    elif kind == 'iron':
        for x0, x1 in ((L, M), (M, R)):
            t.hatch(t.rect_pts(x0, a, x1 - x0, b - a), gap=0.03, angle=0, width=0.5)
            t.outline(t.rect_pts(x0, a, x1 - x0, b - a), 1.6)
            for k in range(1, 6):
                xx = x0 + (x1 - x0) * k / 6
                c.setFillGray(0); c.circle(*t.P(xx, a + 0.035), 0.012 * inch, fill=1, stroke=0)
                c.circle(*t.P(xx, b - 0.035), 0.012 * inch, fill=1, stroke=0)
    elif kind == 'portcullis':
        t.line((L, 0.25), (R, 0.25), 2.0)
        xx = L + 0.06
        while xx < R - 0.02:
            t.line((xx, a), (xx, b), 1.3)
            t.fill([(xx - 0.015, b), (xx + 0.015, b), (xx, b + 0.04)], gray=0)
            xx += 0.085
    elif kind == 'secret':
        c.setFillGray(1)
        c.setFont('Helvetica-Bold', 11)
        px, py = t.P(M, 0.25)
        c.setFillGray(0); c.rect(px - 7, py - 6.5, 14, 13, fill=1, stroke=0)
        c.setFillGray(1); c.drawCentredString(px, py - 4, 'S')
        t.line((M - 0.45, 0.15), (M - 0.45, 0.35), 1.0, 0, dash=[2, 2])
        t.line((M + 0.45, 0.15), (M + 0.45, 0.35), 1.0, 0, dash=[2, 2])
    elif kind == 'broken':
        t.outline(t.rect_pts(L, a, 0.38, b - a), 1.4)
        t.outline(t.rect_pts(R - 0.3, a, 0.3, b - a), 1.4)
        for _ in range(9):
            u = t.rng.uniform(L + 0.5, R - 0.4); v = t.rng.uniform(0.08, 0.42)
            ang = t.rng.uniform(0, math.pi); ln = t.rng.uniform(0.06, 0.13)
            t.outline(t.rect_pts(u, v, ln, 0.02), 0.8) if ang < 1.5 else t.outline(t.rect_pts(u, v, 0.02, ln * 0.6), 0.8)
    elif kind == 'arch':
        for xx in (L, R - 0.06):
            t.fill(t.rect_pts(xx, 0.08, 0.06, 0.34), gray=0)
        t.line((L + 0.06, 0.25), (R - 0.06, 0.25), 0.8, 0, dash=[4, 3])
    elif kind == 'sealed':
        for k in range(1, 9):
            xx = L + (R - L) * k / 9
            t.line((xx, 0.15), (xx, 0.35), 0.6, 1.0)
    t.cut_line()


def ladder(c, x, y, seed):
    t = Tile(c, x, y, 1, 1, seed)
    m = 0.2
    o = t.rect_pts(m, m, 1 - 2 * m, 1 - 2 * m)
    t.hatch(o, gap=0.035, cross=True, width=0.5)
    # ladder knocked out in paper color would need white; draw it in white with black outline
    c.setFillGray(1)
    for r in (0.38, 0.62):
        t.fill(t.rect_pts(r - 0.025, m - 0.08, 0.05, 1 - 2 * m + 0.08), gray=1, stroke=0, width=0.8)
    v = m + 0.06
    while v < 1 - m:
        t.fill(t.rect_pts(0.405, v, 0.19, 0.03), gray=1, stroke=0, width=0.6)
        v += 0.09
    t.outline(o, 2.0)
    t.cut_line()


def trapdoor(c, x, y, seed):
    t = Tile(c, x, y, 1, 1, seed)
    m = 0.17
    t.outline(t.rect_pts(m, m, 1 - 2 * m, 1 - 2 * m), 1.6)
    for k in range(1, 5):
        v = m + (1 - 2 * m) * k / 5
        t.line((m, v), (1 - m, v), 0.5, 0.3)
    for v in (m + 0.12, 1 - m - 0.12):
        t.fill(t.rect_pts(m + 0.02, v - 0.02, 1 - 2 * m - 0.04, 0.04), gray=0)
    c.setStrokeGray(0); c.setLineWidth(1.6)
    c.circle(*t.P(0.5, 0.5), 0.07 * inch, fill=0, stroke=1)
    t.cut_line()


def spiral(c, x, y, seed):
    t = Tile(c, x, y, 1, 1, seed)
    cx, cy = t.P(0.5, 0.5)
    c.setStrokeGray(0)
    c.setLineWidth(2.2); c.circle(cx, cy, 0.44 * inch, fill=0, stroke=1)
    c.setLineWidth(0.9)
    for k in range(12):
        a = math.radians(k * 30)
        c.line(cx + math.cos(a) * 0.08 * inch, cy + math.sin(a) * 0.08 * inch,
               cx + math.cos(a) * 0.44 * inch, cy + math.sin(a) * 0.44 * inch)
    c.setFillGray(0); c.circle(cx, cy, 0.08 * inch, fill=1, stroke=0)
    t.cut_line()


# ======================================================================= test sheet
def header(c, title):
    c.setFillGray(0)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(0.3 * inch, (PAGE_H - 0.45) * inch, f"Dungeon Tiles  |  {title}")
    c.setFont('Helvetica', 7.5)
    c.drawString(0.3 * inch, (PAGE_H - 0.62) * inch,
                 "Print at 100% / Actual Size. The ruler must measure exactly 2 inches, and each grid square 1 inch.")
    rx, ry = 6.15 * inch, (PAGE_H - 0.52) * inch
    c.setLineWidth(0.8); c.setStrokeGray(0)
    c.line(rx, ry, rx + 2 * inch, ry)
    for i in range(9):
        tl = 0.12 if i % 4 == 0 else 0.06
        c.line(rx + i * 0.25 * inch, ry, rx + i * 0.25 * inch, ry + tl * inch)
    c.setFont('Helvetica', 6)
    for i in range(3):
        c.drawCentredString(rx + i * inch, ry - 0.1 * inch, f"{i}\"")


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdf', 'Dungeon Tiles - Line Art Test Sheet.pdf')
    c = canvas.Canvas(out, pagesize=(PAGE_W * inch, PAGE_H * inch))
    c.setTitle('Dungeon Tiles - Line Art Test Sheet')
    header(c, 'Line Art Test Sheet')
    floor(c, 0, 0, 2, 4, [(0, 0, T, 4), (2 - T, 0, T, 4)], 1)
    floor(c, 2, 0, 2, 2, [(0, 0, 2, T), (0, T, T, 2 - T), (2 - T, 2 - T, T, T)], 2)
    floor(c, 4, 0, 2, 2, [(0, 0, 2, T), (0, 2 - T, T, T), (2 - T, 2 - T, T, T)], 3)
    floor(c, 6, 0, 2, 2, [(0, 0, T, T), (2 - T, 0, T, T), (0, 2 - T, T, T), (2 - T, 2 - T, T, T)], 4)
    floor(c, 2, 2, 2, 2, [(0, 0, 2, T), (0, T, T, 2 - T), (2 - T, T, T, 2 - T)], 5)
    floor(c, 4, 2, 2, 2, [(0, 0, 2, T), (0, T, T, 2 - T)], 6)
    floor(c, 6, 2, 2, 2, [(0, 0, 2, T)], 7)
    floor(c, 0, 4, 4, 4, [], 8)
    stairs(c, 4, 4, 9)
    pit(c, 6, 4, 10, spikes=True)
    collapsed(c, 6, 6, 11)
    for i, k in enumerate(['wood', 'locked', 'iron', 'portcullis', 'secret', 'broken', 'arch', 'sealed']):
        door(c, (i % 2) * 2, 8 + (i // 2) * 0.5, k, 20 + i)
    ladder(c, 4, 8, 13)
    trapdoor(c, 5, 8, 14)
    spiral(c, 4, 9, 15)
    pit(c, 5, 9, 16, w=1, h=1)
    floor(c, 6, 8, 2, 2, [(2 - T, 2 - T, T, T)], 12)
    c.save()
    print('ok')
