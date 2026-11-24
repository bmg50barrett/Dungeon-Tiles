# Dungeon Tiles

Printable, modular dungeon tiles in black line art, made for a Chessex battle mat with a 1 inch grid. One square is 1 inch, which is 5 feet in the game. Tiles are cut to whole inches, so they sit right on top of the mat grid and line up with it.

## What's in here

| File | What it is |
|---|---|
| `pdf/Dungeon Tiles - Full Set.pdf` | The full set: 6 letter-size sheets |
| `pdf/Dungeon Tiles - Line Art Test Sheet.pdf` | One sheet with one of each tile type. Print this first to check scale and contrast |
| `src/lineart.py` | Draws the tiles (and builds the test sheet when run on its own) |
| `src/full_set.py` | Lays the full set out across the sheets |

## Printing

These are designed to print best this way:

- **Print at 100% / Actual Size.** Turn off "Fit to page", "Shrink oversized pages" and any other scaling in the print dialog. Even a few percent of shrink makes long corridors drift off the mat grid.
- **Use heavy gray cardstock.** The floors are left unprinted, so the gray paper becomes the stone floor. White stock works too, but the tiles look flatter.
- **Letter paper (8.5 x 11).** The tiles fill an 8 x 10 inch area with a 0.25 inch margin, which fits printers that can't print to the edge.
- **Check the ruler.** Every sheet has a 2 inch ruler in the top right corner. Measure it before printing the rest. If it isn't exactly 2 inches, your printer is scaling the page.

## Laminating and cutting

1. Laminate the whole sheet first.
2. Cut along the thin gray lines with a paper trimmer. The tiles butt up against each other, so one cut separates two tiles.

Cutting first and laminating each tile separately also works, but it takes longer and the edges come out less even. Laminated tiles take wet-erase and dry-erase markers.

## The full set

| Group | Pieces |
|---|---|
| Corridors (10 ft wide) | 6 straight 2x4, 4 straight 2x2, 4 corners, 3 T-junctions, 2 crossroads, 2 dead ends |
| Rooms | 8 outer corners, 15 edges 2x2, 6 edges 2x4, 4 inner corners, 4 floors 4x4, 4 floors 2x4, 14 floors 2x2 |
| Stairs and pits | 2 stairs, 1 spiked pit, 1 open pit, 2 collapsed floors, 2 small pits, 2 ladders, 2 trapdoors, 2 spiral stairs |
| Doors | 7 wooden, 3 locked, 2 iron, 2 portcullis, 4 secret, 2 broken, 2 archway, 2 sealed |

That's 74 tiles plus 24 door strips, enough for a dungeon about 4 by 6 feet on the table.

## How the pieces fit together

- **Walls are drawn inside the tile edge**, 0.15 inch thick. This keeps every tile on the grid. The tradeoff is that squares along a wall lose a thin strip of floor, though a 1 inch mini base still fits.
- **Corridors and rooms share one system.** Build a room from outer corners, edges and plain floors. Use the inner corner piece (a small wall post) where a room turns an L-shaped corner.
- **To join a corridor to a room,** put a plain floor piece in the room's wall where you'd normally put an edge piece.
- **Doors are 2 x 0.5 inch strips** that lie across a 10 foot opening, centered on the joint between two tiles.
- **Stairs work both ways.** The step lines bunch together at the low end. Turn the tile around to make them go up instead of down.

## Known gaps

- Corridors only come 10 feet wide. There are no 5 foot corridors yet.
- There are no natural cave pieces or furniture (tables, chests, altars and so on).
- Doors only fit 10 foot openings.
- The pieces above take up a bit less than 6 sheets, so the leftover spaces are filled with extra plain floors and room edges (already counted in the table).

## Rebuilding the PDFs

The tiles are drawn as vector art with Python and ReportLab. Random details like cracks and rubble use fixed seeds, so rebuilding gives you the same tiles every time.

```
pip install -r requirements.txt
python src/full_set.py    # writes pdf/Dungeon Tiles - Full Set.pdf
python src/lineart.py     # writes pdf/Dungeon Tiles - Line Art Test Sheet.pdf
```

To change how many of each piece you get, edit the `add(...)` lines and the door counts near the top of `src/full_set.py`.
