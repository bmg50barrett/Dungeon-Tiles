# Dungeon Tiles

Printable, modular dungeon tiles in black line art, made for a Chessex battle mat with a 1 inch grid. One square is 1 inch, which is 5 feet in the game. Tiles are cut to whole inches, so they sit right on top of the mat grid and line up with it.

## What's in here

| File | What it is |
|---|---|
| `pdf/Dungeon Tiles - Full Set.pdf` | The full set: 6 letter-size sheets |
| `pdf/Dungeon Tiles - Cut Guide.pdf` | A matching page for each sheet showing every tile's outline and name, with numbered cuts |
| `pdf/Dungeon Tiles - Full Rooms.pdf` | Ready-made 4x4 and 5x5 rooms in every door layout, with spare space filled by 5 ft and 10 ft hallways (4 sheets, single-sided) |
| `pdf/Dungeon Tiles - Full Rooms Cut Guide.pdf` | Cut guide for Full Rooms |
| `pdf/Dungeon Tiles - Full Rooms Double-Sided.pdf` | The same rooms printed front and back, with a different door layout on each side (3 sheets, 6 pages) |
| `pdf/Dungeon Tiles - Full Rooms Double-Sided Cut Guide.pdf` | Cut guide for the double-sided rooms, showing both faces of each piece |
| `pdf/Dungeon Tiles - Line Art Test Sheet.pdf` | One sheet with one of each tile type. Print this first to check scale and contrast |
| `src/lineart.py` | Draws the tiles (and builds the test sheet when run on its own) |
| `src/full_set.py` | Lays the full set out across the sheets |
| `src/cut_guide.py` | Builds the cut guide from the same layout |
| `src/rooms.py` | Builds Full Rooms and its cut guide |
| `src/rooms_duplex.py` | Builds the double-sided rooms and their cut guide |

## Printing

These are designed to print best this way:

- **Print at 100% / Actual Size.** Turn off "Fit to page", "Shrink oversized pages" and any other scaling in the print dialog. Even a few percent of shrink makes long corridors drift off the mat grid.
- **Use heavy gray cardstock.** The floors are left unprinted, so the gray paper becomes the stone floor. White stock works too, but the tiles look flatter.
- **Letter paper (8.5 x 11).** The tiles fill an 8 x 10 inch area with a 0.25 inch margin, which fits printers that can't print to the edge.
- **Check the ruler.** Every sheet has a 2 inch ruler in the top right corner. Measure it before printing the rest. If it isn't exactly 2 inches, your printer is scaling the page.

## Laminating and cutting

1. Laminate the whole sheet first.
2. Open the cut guide page for that sheet. Trim the four margins (marked T), then make the numbered cuts in order. Every cut runs straight across the piece you're holding, so a paper trimmer works for all of them.
3. The cuts follow the thin gray lines on the tiles. The tiles butt up against each other, so one cut separates two tiles.

Cutting first and laminating each tile separately also works, but it takes longer and the edges come out less even. Laminated tiles take wet-erase and dry-erase markers.

## The full set

| Group | Pieces |
|---|---|
| Corridors (10 ft wide) | 6 straight 2x4, 4 straight 2x2, 4 corners, 3 T-junctions, 2 crossroads, 2 dead ends |
| Rooms | 8 outer corners, 15 edges 2x2, 6 edges 2x4, 4 inner corners, 4 floors 4x4, 4 floors 2x4, 14 floors 2x2 |
| Stairs and pits | 2 stairs, 1 spiked pit, 1 open pit, 2 collapsed floors, 2 small pits, 2 ladders, 2 trapdoors, 2 spiral stairs |
| Doors | 7 wooden, 3 locked, 2 iron, 2 portcullis, 4 secret, 2 broken, 2 archway, 2 sealed |

That's 74 tiles plus 24 door strips, enough for a dungeon about 4 by 6 feet on the table.

## Full Rooms

Most rooms in play are 4x4 (20 ft) or 5x5 (25 ft), so these come pre-built with walls on all four sides. Each size comes in every door layout: 1 door, 2 doors opposite, 2 doors at a corner, 3 doors and 4 doors. Any other layout is one of these turned around on the table.

- Doorways are centered in the wall. 5x5 rooms have 5 ft doorways, since an odd-length wall can only center a 1-square opening. 4x4 rooms have 10 ft doorways, which fit the 10 ft door strips.
- Doorways are open gaps, and each one is exactly as wide as the hallway floor: the room wall runs 0.15 inch into the doorway square on each side, matching the hallway's own walls, so walls line up when a hallway meets the door. Lay a door strip over one if you want a door there.
- Spare space on the sheets is filled with 5 ft and 10 ft hallways: straights, plus small 5 ft corners, T-junctions, crossroads and dead ends.
- 5 ft hallways are tight. With walls on both sides there's about 0.7 inch of floor, so a 1 inch mini base sits slightly over the walls.

### Double-sided rooms

The double-sided file puts a different room on the back of each piece to save cardstock. Its 3 sheets hold 3 5x5 rooms and 5 4x4 rooms, so every door layout appears at least once in each size.

- Pages alternate front, back, front, back. The back pages are mirrored so they line up behind the fronts.
- Print duplex with "flip on long edge". If your printer won't auto-duplex heavy cardstock, print the odd pages, then feed the stack back in for the even pages. Expect a test or two to find which way your printer wants the stack loaded.
- Print sheet 1 front and back first and hold it up to a light. Most printers shift the back by a millimeter or two. The walls sit inside the tile edges, so a small shift is mostly hidden.
- Cut with the front side up.

## How the pieces fit together

- **Walls are drawn inside the tile edge**, 0.15 inch thick. This keeps every tile on the grid. The tradeoff is that squares along a wall lose a thin strip of floor, though a 1 inch mini base still fits.
- **Corridors and rooms share one system.** Build a room from outer corners, edges and plain floors. Use the inner corner piece (a small wall post) where a room turns an L-shaped corner.
- **To join a corridor to a room,** put a plain floor piece in the room's wall where you'd normally put an edge piece. Note that this leaves an opening 0.3 inch wider than the corridor floor, so the walls don't quite meet. The Full Rooms pieces have properly sized doorways.
- **Doors are 2 x 0.5 inch strips** that lie across a 10 foot opening, centered on the joint between two tiles.
- **Stairs work both ways.** The step lines bunch together at the low end. Turn the tile around to make them go up instead of down.

## Known gaps

- The modular full set only has 10 foot corridors. 5 foot hallways come only in the Full Rooms files.
- There are no natural cave pieces or furniture (tables, chests, altars and so on).
- The modular full set has no doorway edge piece yet, so a corridor joining a room built from edge pieces won't have its walls line up exactly.
- Door strips only fit 10 foot openings. There are no strips yet for the 5 foot doorways on the 5x5 rooms.
- The pieces above take up a bit less than 6 sheets, so the leftover spaces are filled with extra plain floors and room edges (already counted in the table).

## Rebuilding the PDFs

The tiles are drawn as vector art with Python and ReportLab. Random details like cracks and rubble use fixed seeds, so rebuilding gives you the same tiles every time.

```
pip install -r requirements.txt
python src/full_set.py    # writes pdf/Dungeon Tiles - Full Set.pdf
python src/cut_guide.py   # writes pdf/Dungeon Tiles - Cut Guide.pdf
python src/rooms.py       # writes Full Rooms and its cut guide
python src/rooms_duplex.py  # writes the double-sided rooms and their cut guide
python src/lineart.py     # writes pdf/Dungeon Tiles - Line Art Test Sheet.pdf
```

To change how many of each piece you get, edit the `add(...)` lines and the door counts near the top of `src/full_set.py`.
