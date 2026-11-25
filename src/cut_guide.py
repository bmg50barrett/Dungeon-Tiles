"""Cut guide for the full set: same layout as the tile sheets, showing each
tile's outline and name, plus numbered guillotine cuts (each cut runs straight
across the piece you are holding, so it works with a paper trimmer)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from lineart import PAGE_W, PAGE_H, OX, OY, header
import modular_set as fs

LABELS = {
    'floor4x4': 'Floor 4x4', 'corridor2x4': 'Corridor 2x4', 'edge2x4': 'Room edge 2x4',
    'floor2x4': 'Floor 2x4', 'stairs': 'Stairs', 'straight': 'Corridor', 'corner': 'Corner',
    'tee': 'T-junction', 'cross': 'Crossroads', 'dead': 'Dead end', 'outer': 'Outer corner',
    'edge': 'Room edge', 'inner': 'Inner corner', 'doorway': 'Doorway edge', 'floor2x2': 'Floor 2x2', 'spikepit': 'Spiked pit',
    'pit': 'Pit', 'collapsed': 'Collapsed', 'pit1': 'Pit', 'ladder': 'Ladder',
    'trapdoor': 'Trapdoor', 'spiral': 'Spiral', 'door': 'Door',
}
TALL = {'corridor2x4', 'edge2x4', 'floor2x4', 'stairs'}
RED = (0.8, 0.1, 0.1)


def pieces_for_page(pi):
    """Return list of (x, y, w, h, label) in squares."""
    out = []
    mini_i = door_i = 0
    minis_groups = [fs.minis[i:i + 4] for i in range(0, len(fs.minis), 4)]
    door_groups = [fs.doors[i:i + 4] for i in range(0, len(fs.doors), 4)]
    # count blocks in placement order across all pages so groups line up with modular_set
    for (pj, col, r, (name, f)) in fs.placed:
        x, y = col * 2, r * 2
        if name == 'minis':
            g = minis_groups[mini_i]; mini_i += 1
            if pj == pi:
                for i, (n, _) in enumerate(g):
                    out.append((x + i % 2, y + i // 2, 1, 1, LABELS[n]))
        elif name == 'doors':
            g = door_groups[door_i]; door_i += 1
            if pj == pi:
                for i, k in enumerate(g):
                    out.append((x, y + i * 0.5, 2, 0.5, f"Door: {k}"))
        elif pj == pi:
            w, h = (4, 4) if name == 'floor4x4' else (2, 4) if name in TALL else (2, 2)
            out.append((x, y, w, h, LABELS[name]))
    return out


def plan_cuts(region, pcs):
    """Guillotine cuts, breadth first. Returns list of (level, (x0, y0, x1, y1)) line segments."""
    cuts = []
    queue = [(region, pcs, 1)]
    while queue:
        (x0, y0, x1, y1), ps, lvl = queue.pop(0)
        if len(ps) <= 1:
            continue
        best = None
        for axis in ('h', 'v'):
            edges = sorted({p[1] for p in ps} | {p[1] + p[3] for p in ps}) if axis == 'h' else \
                    sorted({p[0] for p in ps} | {p[0] + p[2] for p in ps})
            lo, hi = (y0, y1) if axis == 'h' else (x0, x1)
            for e in edges:
                if not (lo < e < hi):
                    continue
                if axis == 'h' and any(p[1] < e < p[1] + p[3] for p in ps):
                    continue
                if axis == 'v' and any(p[0] < e < p[0] + p[2] for p in ps):
                    continue
                # prefer the cut that splits the pile most evenly
                score = abs((e - lo) - (hi - e))
                if best is None or score < best[0]:
                    best = (score, axis, e)
        if best is None:
            continue
        _, axis, e = best
        if axis == 'h':
            cuts.append((lvl, (x0, e, x1, e)))
            a = [p for p in ps if p[1] + p[3] <= e]; b = [p for p in ps if p[1] >= e]
            queue += [((x0, y0, x1, e), a, lvl + 1), ((x0, e, x1, y1), b, lvl + 1)]
        else:
            cuts.append((lvl, (e, y0, e, y1)))
            a = [p for p in ps if p[0] + p[2] <= e]; b = [p for p in ps if p[0] >= e]
            queue += [((x0, y0, e, y1), a, lvl + 1), ((e, y0, x1, y1), b, lvl + 1)]
    return cuts


def P(u, v):
    return ((OX + u) * inch, (PAGE_H - OY - v) * inch)


def draw_page(c, pi, n_pages):
    return draw_guide(c, f"Modular Set Cut Guide  |  Sheet {pi + 1} of {n_pages}", pieces_for_page(pi))


def draw_guide(c, title, pcs):
    xs = [p[0] + p[2] for p in pcs]; ys = [p[1] + p[3] for p in pcs]
    W, H = max(xs), max(ys)
    # header with calibration ruler
    header(c, title, "Laminate first. Trim the margins (T), then cut in number order. "
                     "Each cut runs across the piece you are holding.")
    # tile outlines and names
    c.setStrokeGray(0.6); c.setLineWidth(0.5)
    for (x, y, w, h, lab) in pcs:
        px, py = P(x, y + h)
        c.rect(px, py, w * inch, h * inch)
        c.setFillGray(0.45)
        size = 6.5 if h >= 1 else 6
        c.setFont('Helvetica', size)
        cx, cy = P(x + w / 2, y + h / 2)
        lines = lab.split('  /  ')
        for li, text in enumerate(lines):
            c.drawCentredString(cx, cy - size / 3 + (len(lines) / 2 - li - 0.5) * (size + 1.5), text)
    # margin trims
    c.setStrokeColorRGB(*RED); c.setLineWidth(1.6); c.setDash([6, 3])
    trims = [((0, 0), (W, 0)), ((0, H), (W, H)), ((0, 0), (0, H)), ((W, 0), (W, H))]
    for a, b in trims:
        c.line(*P(*a), *P(*b))
    c.setDash([])
    for (a, b) in trims:
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        label(c, mx, my, 'T')
    # numbered cuts
    cuts = plan_cuts((0, 0, W, H), pcs)
    for i, (lvl, (x0, y0, x1, y1)) in enumerate(cuts, 1):
        c.setStrokeColorRGB(*RED); c.setLineWidth(1.6 if lvl == 1 else 1.1 if lvl == 2 else 0.8)
        c.line(*P(x0, y0), *P(x1, y1))
    for i, (lvl, (x0, y0, x1, y1)) in enumerate(cuts, 1):
        # label near the start of the cut, nudged inside the piece
        if y0 == y1:
            lx, ly = x0 + min(0.35, (x1 - x0) / 2), y0
        else:
            lx, ly = x0, y0 + min(0.35, (y1 - y0) / 2)
        label(c, lx, ly, str(i))
    return len(cuts)


def label(c, u, v, text):
    px, py = P(u, v)
    r = 6.2 if len(text) < 3 else 7.5
    c.setFillGray(1); c.setStrokeColorRGB(*RED); c.setLineWidth(0.9)
    c.circle(px, py, r, fill=1, stroke=1)
    c.setFillColorRGB(*RED); c.setFont('Helvetica-Bold', 6.5)
    c.drawCentredString(px, py - 2.3, text)


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdf', 'Dungeon Tiles - Modular Set Cut Guide.pdf')
    c = canvas.Canvas(out, pagesize=(PAGE_W * inch, PAGE_H * inch))
    c.setTitle('Dungeon Tiles - Modular Set Cut Guide')
    n = len(fs.pages)
    for pi in range(n):
        k = draw_page(c, pi, n)
        print(f"sheet {pi + 1}: {k} cuts")
        c.showPage()
    c.save()
