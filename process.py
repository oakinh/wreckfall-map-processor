import json

# Configuration
TILE_WIDTH = 32
TILE_HEIGHT = 32
TILESET_COLUMNS = 4  # Number of columns in the tileset
TILESET_ROWS = 4     # Number of rows in the tileset

# Animated Tilesheet Configuration
ANIMATED_TILE_ID = 16
ANIMATED_TILE_COLUMNS = 21  # Frames per row in the animated tilesheet
ANIMATED_TILE_ROWS = 1     # Rows in the animated tilesheet
ANIMATED_TILE_FRAMES = 21   # Total number of animation frames

# Raw map for map1
raw_map = [
    [14, 13, 14, 15, 13, 16, 12, 13, 14, 14],
    [12, 10, 11, 11, 11, 16, 11, 11, 11, 12],
    [12, 10, 10, 8, 12, 16, 10, 8, 8, 12],
    [15, 10, 10, 8, 12, 16, 10, 8, 8, 13],
    [14, 10, 10, 8, 15, 16, 10, 8, 8, 15],
    [12, 10, 4, 5, 5, 5, 6, 8, 8, 12],
    [12, 10, 10, 10, 8, 16, 10, 8, 8, 12],
    [13, 10, 10, 10, 8, 16, 10, 8, 8, 13],
    [14, 9, 9, 9, 9, 16, 9, 9, 8, 14],
    [15, 13, 14, 12, 13, 16, 12, 13, 14, 12]
]

# Metadata for each tile
tile_metadata = {
    0: {"passable": False, "type": "empty"},
    4: {"passable": True, "type": "bridge"},
    5: {"passable": True, "type": "bridge"},
    6: {"passable": True, "type": "bridge"},
    8: {"passable": True, "type": "floor"},
    9: {"passable": True, "type": "floor"},
    10: {"passable": True, "type": "floor"},
    11: {"passable": True, "type": "floor"},
    12: {"passable": False, "type": "wall"},
    13: {"passable": False, "type": "wall"},
    14: {"passable": False, "type": "wall"},
    15: {"passable": False, "type": "wall"},
    16: {"passable": False, "type": "water", "animated": True, "frames": ANIMATED_TILE_FRAMES}
}

def calculate_uvs(tile_id):
    x = tile_id % TILESET_COLUMNS
    y = tile_id // TILESET_COLUMNS

    # Invert row to match typical OpenGL coordinate system
    inverted_y = (TILESET_ROWS - 1) - y

    u0 = x / TILESET_COLUMNS
    v0 = inverted_y / TILESET_ROWS
    u1 = (x + 1) / TILESET_COLUMNS
    v1 = (inverted_y + 1) / TILESET_ROWS
    return [u0, v0, u1, v1]

def calculate_uvs_for_animated(frame):
    """Calculate UVs for a specific frame of the animated tile."""
    x = frame % ANIMATED_TILE_COLUMNS
    y = frame // ANIMATED_TILE_COLUMNS
    u0 = x / ANIMATED_TILE_COLUMNS
    v0 = y / ANIMATED_TILE_ROWS
    u1 = (x + 1) / ANIMATED_TILE_COLUMNS
    v1 = (y + 1) / ANIMATED_TILE_ROWS
    return [u0, v0, u1, v1]

def process_map(raw_map, tile_metadata):
    """Process the raw map and attach metadata and UVs to each tile."""
    processed_map = []
    for row in raw_map:
        processed_row = []
        for tile_id in row:
            tile_info = tile_metadata.get(tile_id, {"passable": True, "type": "unknown"})
            tile_info["tile_id"] = tile_id
            if tile_id == ANIMATED_TILE_ID:
                tile_info["uv_frames"] = [
                    calculate_uvs_for_animated(frame) for frame in range(ANIMATED_TILE_FRAMES)
                ]
            else:
                tile_info["uv"] = calculate_uvs(tile_id)
            processed_row.append(tile_info)
        processed_map.append(processed_row)
    return processed_map

# Process the map
processed_map = process_map(raw_map, tile_metadata)

# Save the processed map as JSON
output_file = "processed_map_inverted.json"
with open(output_file, "w") as f:
    json.dump(processed_map, f, indent=4)
print(f"Processed map saved to {output_file}")
