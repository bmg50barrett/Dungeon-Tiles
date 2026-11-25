# Tile Catalog

`tiles.json` lists every tile design and every physical piece in the printed files, so other tools can work out which pieces a map needs. A dungeon generator's bill of materials is the main use.

Don't edit `tiles.json` by hand. It's built by `src/catalog.py` from the same definitions that draw the sheets, so it always matches what's printed:

```
python src/catalog.py
```

Right now the catalog covers the Full Rooms and 4x4 Rooms files (single-sided and double-sided). The Modular Set isn't in it yet.

## Structure

```
catalog_version          bumps when the format changes
grid                     1 square = 1 inch = 5 feet
wall_thickness_inches    walls are drawn inside the piece's edge
edge_convention          how to read openings (below)
faces                    every tile design, keyed by ID
editions                 every printed file and the physical pieces in it
```

### Faces

A face is one tile design, like "4x4 room, 2 doors at a corner". IDs are stable: once published, an ID is never renamed or reused, so a saved BOM stays valid.

```json
"R4-2C": {
  "name": "Room 4x4 (20 ft), 2 doors, corner",
  "kind": "room",
  "size": [4, 4],
  "door_width_ft": 10,
  "openings": { "N": [[1, 2]], "E": [[1, 2]], "S": [], "W": [] }
}
```

| ID | What it is |
|---|---|
| `R4-1`, `R4-2O`, `R4-2C`, `R4-3`, `R4-4` | 4x4 rooms with 10 ft doorways: 1 door, 2 opposite, 2 at a corner, 3, 4 |
| `R5-1`, `R5-2O`, `R5-2C`, `R5-3`, `R5-4` | 5x5 rooms with 5 ft doorways, same layouts |
| `R4P-1`, `R4P-2O`, `R4P-2C`, `R4P-3`, `R4P-4` | 4x4 rooms with 5 ft doorways, same layouts. Every door is one square in from the left end of its wall going clockwise, so every opening reads `[1, 1]` |
| `H5-S4`, `H5-S5` | 5 ft hall, straight, 4 or 5 squares long |
| `H10-S5` | 10 ft hall, straight, 5 squares long |
| `H5-L`, `H5-T`, `H5-X`, `H5-D` | 5 ft hall corner, T-junction, crossroads, dead end |

### Reading openings

`size` is `[width, height]` in squares, in the face's canonical orientation. `openings` lists the gaps in the wall on each side as `[offset, width]` in squares. Anything not listed is wall.

Offsets run clockwise around the piece:

- **N** is measured from its west end
- **E** from its north end
- **S** from its east end
- **W** from its south end

The point of measuring clockwise is that rotation becomes simple. Every piece can be turned to any of 4 orientations, and turning it 90 degrees clockwise just moves each side's openings to the next side (N to E, E to S, S to W, W to N) while swapping width and height. Offsets don't change.

An opening's width is the passage width: 1 square for 5 ft, 2 squares for 10 ft. The walls on either side of a doorway match a hallway's walls, so any opening lines up with a hallway of the same width.

### Editions

An edition is one printed file. Each lists its physical pieces:

```json
{ "faces": ["R5-1", "R5-2O"], "sheet": 1, "at": [0, 0] }
```

- `faces` has one ID for a single-sided piece, or two (front, back) for a double-sided one. A double-sided piece can only show one face at a time, so a BOM should count physical pieces, not faces.
- `sheet` is the sheet number in that file, and `at` is the piece's top-left corner on the front of the sheet, in squares from the top-left of the tile area.
- `faces_available` totals how many pieces carry each face in one printing of that edition.

## What a BOM tool still has to handle

- Matching map features to faces, allowing all 4 rotations.
- For double-sided pieces, choosing which face each piece shows, since two faces share one piece.
- Turning "pieces needed" into "sheets to print" when a design is needed more often than one printing provides.
- Reporting anything the catalog can't build (a 3x3 room, an off-center door, a 5 ft hall into a 4x4 room's 10 ft doorway) instead of dropping it.
