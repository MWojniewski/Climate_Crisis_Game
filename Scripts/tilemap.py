import pygame
import json

NEIGHBOUR_OFFSETS = [
    (-1, -1),
    (-1, 2),
    (0, 2),
    (1, 2),
    (2, 2),
    (2, 1),
    (2, 0),
    (2, -1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (0, 0),
    (1, 0),
    (0, 1),
    (1, -1),
    (-1, 1),
]


PHYSICS_TILES = {"metal", "diode_metal"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tile_size
                matches[-1]["pos"][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, pos):
        grid_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tiles = []
        for offset in NEIGHBOUR_OFFSETS:
            if (
                str(offset[0] + grid_pos[0]) + ";" + str(offset[1] + grid_pos[1])
                in self.tilemap
            ):
                tiles.append(
                    str(offset[0] + grid_pos[0]) + ";" + str(offset[1] + grid_pos[1])
                )
        return tiles

    def save(self, path):
        map_file = open(path, mode="w")
        json.dump(
            {
                "tilemap": self.tilemap,
                "tile_size": self.tile_size,
                "offgrid": self.offgid_tiles,
            },
            map_file,
        )
        map_file.close()

    def load(self, path):
        map_file = open(path, "r")
        map_data = json.load(map_file)
        map_file.close()

        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgid_tiles = map_data["offgrid"]

    def solid_check(self, pos):
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def physics_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if self.tilemap[tile]["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        self.tilemap[tile]["pos"][0] * self.tile_size,
                        self.tilemap[tile]["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )
