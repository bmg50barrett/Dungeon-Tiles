# Dungeon Tiles

Printable, modular dungeon tiles in black line art, made for a Chessex battle mat with a 1 inch grid. One square is 1 inch, which is 5 feet in the game. Tiles are cut to whole inches, so they sit right on top of the mat grid and line up with it.

## What's in here

| File | What it is |
|---|---|
| `pdf/Dungeon Tiles - 4x4 Rooms.pdf` | 4x4 rooms with 5 ft doors for 5 ft hallways, in every door layout, plus 5 ft hallway pieces (2 sheets, single-sided) |
| `pdf/Dungeon Tiles - 4x4 Rooms Cut Guide.pdf` | Cut guide for the 4x4 Rooms |
| `pdf/Dungeon Tiles - 4x4 Rooms Double-Sided.pdf` | The same rooms printed front and back (2 sheets, 4 pages) |
| `pdf/Dungeon Tiles - 4x4 Rooms Double-Sided Cut Guide.pdf` | Cut guide for the double-sided 4x4 Rooms |
| `pdf/Dungeon Tiles - 5 ft Hallways.pdf` | A sheet of 5 ft hallway pieces: straights 4 and 5 long, 1-square straights, corners, T-junctions, a crossroads and a dead end |
| `pdf/Dungeon Tiles - 5 ft Hallways Cut Guide.pdf` | Cut guide for 5 ft Hallways |
| `pdf/Dungeon Tiles - 5 ft Hallways Double-Sided.pdf` | The same sheet printed front and back, with a different piece on the back of each small piece |
| `pdf/Dungeon Tiles - 5 ft Hallways Double-Sided Cut Guide.pdf` | Cut guide for the double-sided 5 ft Hallways |
| `pdf/Dungeon Tiles - 4x4 Room Pack.pdf` | One sheet of the most used 4x4 rooms (1 door x2, 2 opposite, 2 at a corner) plus hallway pieces. Print as many as you need |
| `pdf/Dungeon Tiles - 5x5 Room Pack A.pdf` | One sheet: 5x5 rooms with 1 door and 2 doors opposite, plus hallway pieces |
| `pdf/Dungeon Tiles - 5x5 Room Pack B.pdf` | One sheet: 5x5 rooms with 2 doors at a corner and 3 doors, plus hallway pieces |
| `pdf/Dungeon Tiles - 4x4 Room Pack Double-Sided.pdf` | One double-sided sheet of 4x4 rooms (1 door / 3 doors, 1 door / corner, opposite / corner, opposite / 4 doors) plus hallway pieces |
| `pdf/Dungeon Tiles - 5x5 Room Pack Double-Sided.pdf` | One double-sided sheet of 5x5 rooms (1 door / corner, opposite / 3 doors) plus hallway pieces |
| `pdf/Dungeon Tiles - 5x6 Rooms.pdf`, `5x7 Rooms.pdf` | Long rooms, 25 x 30 ft and 25 x 35 ft, with 5 ft doors, in all 9 door layouts (5 sheets each, single-sided). See *Long rooms* below |
| `pdf/Dungeon Tiles - 5x6 Rooms Double-Sided.pdf`, `5x7 Rooms Double-Sided.pdf` | The same long rooms printed front and back (3 sheets each) |
| `pdf/Dungeon Tiles - 5x6 Room Pack A.pdf`, `B`, `C` (and the same for 5x7) | One sheet each of the most used long rooms: A is 1 door (end, side), B is 2 doors (both ends, both sides), C is 2 doors at a corner (right, left) |
| `pdf/Dungeon Tiles - 5x6 Room Pack Double-Sided A.pdf`, `B` (and the same for 5x7) | One double-sided sheet each: A is 1 door end / both ends and 1 door side / both sides; B is 1 door end / corner right and 1 door side / corner left |
| `pdf/Dungeon Tiles - Doorless Rooms All Sizes.pdf` | Rooms with no doors, for door markers: one sheet each of 4x4, 4x5, 4x6, 4x7, 4x8, 5x5, 5x6, 5x7, 5x8 and 6x6 (10 sheets). See *Doorless rooms* below |
| `pdf/Dungeon Tiles - 4x4 Doorless Rooms.pdf` (and the same for each size) | The same sheets one size at a time, to print as many as you need |
| `pdf/Dungeon Tiles - Modular Set.pdf` | Build-your-own pieces: corridors, room walls, corners and floors to make a room of any size, plus stairs, pits and doors (6 sheets) |
| `pdf/Dungeon Tiles - Modular Set Cut Guide.pdf` | Cut guide for the Modular Set: a matching page for each sheet showing every tile's outline and name, with numbered cuts |
| `pdf/Dungeon Tiles - Full Rooms.pdf` | Ready-made 4x4 and 5x5 rooms in every door layout, with spare space filled by 5 ft and 10 ft hallways (4 sheets, single-sided) |
| `pdf/Dungeon Tiles - Full Rooms Cut Guide.pdf` | Cut guide for Full Rooms |
| `pdf/Dungeon Tiles - Full Rooms Double-Sided.pdf` | The same rooms printed front and back, with a different door layout on each side (3 sheets, 6 pages) |
| `pdf/Dungeon Tiles - Full Rooms Double-Sided Cut Guide.pdf` | Cut guide for the double-sided rooms, showing both faces of each piece |
| `catalog/tiles.json` | Machine-readable list of every tile design and physical piece in the Full Rooms, 4x4 Rooms, 5 ft Hallways and Room Pack files, for tools like a dungeon generator's bill of materials. See `catalog/README.md` |
| `src/rooms4.py` | Builds the 4x4 Rooms (single- and double-sided) and their cut guides |
| `src/halls.py` | Builds the 5 ft Hallways sheets and their cut guides |
| `src/packs.py` | Builds the Room Packs and their cut guides |
| `src/longrooms.py` | Builds the 5x6 and 5x7 rooms, their packs and their cut guides |
| `src/doorless.py` | Builds the doorless rooms and their cut guides |
| `src/catalog.py` | Builds `catalog/tiles.json` from the room definitions |
| `src/lineart.py` | Draws the tiles and the page header with its calibration ruler |
| `src/modular_set.py` | Lays the Modular Set out across the sheets |
| `src/cut_guide.py` | Builds the cut guide from the same layout |
| `src/rooms.py` | Builds Full Rooms and its cut guide |
| `src/rooms_duplex.py` | Builds the double-sided rooms and their cut guide |

## Printing

These are designed to print best this way:

- **Print at 100% / Actual Size.** Turn off "Fit to page", "Shrink oversized pages" and any other scaling in the print dialog. Even a few percent of shrink makes long corridors drift off the mat grid.
- **Use heavy gray cardstock.** The floors are left unprinted, so the gray paper becomes the stone floor. White stock works too, but the tiles look flatter.
- **Letter paper (8.5 x 11).** The tiles fill an 8 x 10 inch area with a 0.25 inch margin, which fits printers that can't print to the edge.
- **Check the ruler.** Every page, including the cut guides and the back pages, has a 2 inch ruler in the top right corner. Print any one page first and measure it. If it isn't exactly 2 inches, your printer is scaling the page.

## Laminating and cutting

1. Laminate the whole sheet first.
2. Open the cut guide page for that sheet. Trim the four margins (marked T), then make the numbered cuts in order. Every cut runs straight across the piece you're holding, so a paper trimmer works for all of them.
3. The cuts follow the thin gray lines on the tiles. The tiles butt up against each other, so one cut separates two tiles.

Cutting first and laminating each tile separately also works, but it takes longer and the edges come out less even. Laminated tiles take wet-erase and dry-erase markers.

## The Modular Set

The Modular Set gives you walls, corners, floors and corridors to build a room of any size or shape yourself. For the common 4x4 and 5x5 rooms, Full Rooms below has them ready-made.

| Group | Pieces |
|---|---|
| Corridors (10 ft wide) | 6 straight 2x4, 4 straight 2x2, 4 corners, 3 T-junctions, 2 crossroads, 2 dead ends |
| Rooms | 8 outer corners, 12 edges 2x2, 6 doorway edges, 6 edges 2x4, 4 inner corners, 4 floors 4x4, 4 floors 2x4, 11 floors 2x2 |
| Stairs and pits | 2 stairs, 1 spiked pit, 1 open pit, 2 collapsed floors, 2 small pits, 2 ladders, 2 trapdoors, 2 spiral stairs |
| Doors | 7 wooden, 3 locked, 2 iron, 2 portcullis, 4 secret, 2 broken, 2 archway, 2 sealed |

That's 74 tiles plus 24 door strips, enough for a dungeon about 4 by 6 feet on the table. The pieces take up a bit less than 6 sheets, so the spare spaces on sheet 6 hold the doorway edges and some extra plain floors and room edges (all counted above).

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

## 4x4 Rooms with 5 ft doors

The Full Rooms 4x4s have 10 ft doorways, so they don't meet 5 ft hallways. These 4x4 rooms have 5 ft doorways instead.

A 5 ft doorway can't sit in the middle of a 4-square wall, so every door is one square in from the left end of its wall, going clockwise around the room. Seen from above, the doors make a pinwheel. Because every door follows that same rule, the same 5 layouts (1 door, 2 opposite, 2 at a corner, 3, 4) cover every 4x4 room once you turn the tile, just like the 5x5 rooms.

- Single-sided: 8 rooms on 2 sheets. The most common layouts (1 door, 2 opposite, 2 at a corner) come twice; 3 doors and 4 doors once each.
- Double-sided: 8 pieces on 2 sheets with a different layout on each face, so 16 faces: 2 opposite x5, 2 at a corner x4, 1 door x3, 3 doors x3, 4 doors x1.
- The rest of each sheet holds 5 ft hallway pieces: straights 4 long, corners, T-junctions, crossroads and dead ends.
- Doorways are sized to the hallway floor, the same as the Full Rooms doorways, so walls line up where a hallway meets a door.

## Long rooms (5x6 and 5x7)

After the squares, the room sizes Dungeon Maker makes most often are longer than they are wide. Its Tile mode can use these two, and its tile list counts them.

The doors follow the same rule as the 4x4 and 5x5 rooms: one square in from the left end of the wall going clockwise, as close to the middle as a 5 ft door can get. On an odd wall (5 or 7 long) that is the middle. On a 6-long wall it is one square clockwise of the middle, like the 4x4 pinwheel. Every 5x7 door is centered.

A square room tile matches itself turned four ways, but a long one only turned end for end, so it takes 9 layouts to cover every room instead of 5. With the room standing tall, the short walls at top and bottom are the *ends* and the long walls the *sides*:

| Layout | Doors | How often a long room needs it |
|---|---|---|
| 1A | 1, in an end | about 21% |
| 1B | 1, in a side | about 22% |
| 2A | 2, both ends | about 12% |
| 2B | 2, both sides | about 13% |
| 2C | 2 at a corner, the side door to the right of the end door | about 10% |
| 2D | 2 at a corner, the side door to the left | about 12% |
| 3A | 3, both ends and a side | under 3% |
| 3B | 3, both sides and an end | under 3% |
| 4 | 4 | rare |

The percentages come from 1,500 tile-mode dungeons using all four room sizes.

- Single-sided: 2 rooms to a sheet, laid on their sides, so 5 sheets carry all 9 layouts plus a second 1B.
- Double-sided: 3 sheets, 12 faces. Common layouts are backed by rare ones, so one piece is seldom wanted for both its faces in the same dungeon.
- Room Packs A, B and C hold the six common layouts on three single sheets. The double-sided packs put a 1-door room on the front of every piece and a 2-door room on the back.
- The strip beside the rooms holds 5-long straights: four on a 5x6 sheet, two on a 5x7 sheet.

## Doorless rooms (for door markers)

The other room tiles have their doorways printed on them, which means a tile for every door layout: 5 per square size and 9 per long size. Doorless rooms skip that. Every room has a solid wall all the way round, and the doors are shown with standing door markers (such as C4Labs' small door markers: a 1 inch door on a round base). One design per size covers every room of that size, whatever its doors.

- Ten sizes: 4x4, 4x5, 4x6, 4x7, 4x8, 5x5, 5x6, 5x7, 5x8 and 6x6. Between them they cover the room sizes Dungeon Maker makes most often.
- One sheet per size, as many of that room as fit, with 5 ft straights in any spare space. The 6x6 sheet also has two 4x4s below the 6x6.
- *Doorless Rooms All Sizes* is all ten sheets in one file, for printing one of everything. The single-size files are for printing more of the sizes you use most.
- To place a door, stand the marker on the room's wall line where a hallway or another room meets it. The marker's base overhangs a little into the squares on both sides. Stood fully open, a marker can stand for an open archway.
- There are no double-sided versions. A piece can only carry the same size on its back, and every room of a size is the same.
- Door markers also work on the tiles with printed doorways: stand one in the gap to show a closed door.

## 5 ft Hallways

A sheet of nothing but 5 ft hallway pieces, for dungeons with more hallway than the room sheets carry. Its mix follows what tile-mode dungeons from Dungeon Maker need, which works out to about one sheet for an average dungeon.

| Piece | Single-sided | Double-sided (faces) |
|---|---|---|
| Straight, 4 long | 11 | 11 |
| Straight, 5 long | 1 | 1 |
| Straight, 1 long | 10 | 20 |
| Corner | 15 | 27 |
| T-junction | 4 | 8 |
| Crossroads | 1 | 2 |
| Dead end | 1 | 2 |

On the double-sided sheet the long straights are the same on both sides, and every small piece has a different back (corner and 1-square straight, corner and T, and so on), so one printing bends towards whatever a dungeon needs.

**You don't need a straight for every length.** A straight that's too long can run under a room tile where the hallway meets a door, or 1 square under the corner, T or crossroads tile it ends at. Lay the straights first and the other tiles on top. With that, the 4- and 5-long straights cover every length except a 1-square stretch between two junctions, which is what the 1-square straight is for.

## Room Packs

The full room sets carry every door layout a few times each, spread over several sheets. That's handy as a starter set, but a dungeon with eight 1-door rooms ends up paying for a lot of rooms it doesn't use. The Room Packs fix that: each is a single sheet of the layouts dungeons use most, meant to be printed as many times as a dungeon needs.

| Pack | Rooms | Plus |
|---|---|---|
| 4x4 Room Pack | 1 door x2, 2 opposite, 2 at a corner | two 4-long straights, 5 corners, 3 one-square straights |
| 5x5 Room Pack A | 1 door, 2 opposite | two 5-long and two 4-long straights, 8 corners, 4 one-square straights |
| 5x5 Room Pack B | 2 at a corner, 3 doors | the same hallway pieces as Pack A |
| 4x4 Room Pack, double-sided | 1 door / 3 doors, 1 door / corner, opposite / corner, opposite / 4 doors | straights, and small pieces backed corner / 1-square straight or corner / T |
| 5x5 Room Pack, double-sided | 1 door / corner, opposite / 3 doors | straights, and small pieces backed the same way |

The mix comes from what 300 tile-mode dungeons from Dungeon Maker needed. Rooms split about evenly between 4x4 and 5x5, and within each size 1 door and 2 opposite are the most common, then 2 at a corner, with 3 doors uncommon and 4 doors rare. The rare layouts still come from the full room sets when a dungeon needs them.

Against those same 300 dungeons (3 to 30 rooms each), Dungeon Maker's tile list now plans:

| | Before the packs | With the packs |
|---|---|---|
| Single-sided, median dungeon | 23 sheets | 12 sheets |
| Single-sided, 9 in 10 dungeons need at most | 45 sheets | 20 sheets |
| Double-sided, median dungeon | 18 sheets | 9 sheets |
| Double-sided, 9 in 10 dungeons need at most | 29 sheets | 15 sheets |

## How the pieces fit together

- **Walls are drawn inside the tile edge**, 0.15 inch thick. This keeps every tile on the grid. The tradeoff is that squares along a wall lose a thin strip of floor, though a 1 inch mini base still fits.
- **Corridors and rooms share one system.** Build a room from outer corners, edges and plain floors. Use the inner corner piece (a small wall post) where a room turns an L-shaped corner.
- **To join a corridor to a room,** put a doorway edge in the room's wall where you'd normally put an edge piece. It has a short wall stub at each end, so the opening is exactly as wide as the corridor floor and the walls line up. A 10 ft door strip fits across it.
- **Doors are 2 x 0.5 inch strips** that lie across a 10 foot opening, centered on the joint between two tiles.
- **Stairs work both ways.** The step lines bunch together at the low end. Turn the tile around to make them go up instead of down.

## Known gaps

- The Modular Set only has 10 foot corridors. 5 foot hallways come only in the Full Rooms files.
- There are no natural cave pieces or furniture (tables, chests, altars and so on).
- Door strips only fit 10 foot openings. There are no strips yet for the 5 foot doorways on the 5x5 rooms.
- 5x5 rooms only come with 5 foot doorways, so a 10 foot hall can't meet a 5x5 room. (4x4 rooms now come with either width.)
- There's no piece that narrows a 10 foot corridor down to a 5 foot hallway.
- The Modular Set's doorway edge only fits 10 foot corridors. There's no 5 foot version.
- Stairs only come 10 feet wide.
- Everything runs square to the grid. There are no diagonal corridors.

## Rebuilding the PDFs

The tiles are drawn as vector art with Python and ReportLab. Random details like cracks and rubble use fixed seeds, so rebuilding gives you the same tiles every time.

```
pip install -r requirements.txt
python src/modular_set.py  # writes pdf/Dungeon Tiles - Modular Set.pdf
python src/cut_guide.py    # writes pdf/Dungeon Tiles - Modular Set Cut Guide.pdf
python src/rooms.py       # writes Full Rooms and its cut guide
python src/rooms_duplex.py  # writes the double-sided rooms and their cut guide
python src/rooms4.py       # writes the 4x4 Rooms and their cut guides
python src/halls.py        # writes the 5 ft Hallways and their cut guides
python src/packs.py        # writes the Room Packs and their cut guides
python src/longrooms.py    # writes the 5x6 and 5x7 rooms, their packs and their cut guides
python src/doorless.py     # writes the doorless rooms and their cut guides
python src/catalog.py      # writes catalog/tiles.json
```

To change how many of each piece you get, edit the `add(...)` lines and the door counts near the top of `src/modular_set.py`.
