import pygame
import json

NEIGHBOUR_OFFSETS = [
    (-1, -1),
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
