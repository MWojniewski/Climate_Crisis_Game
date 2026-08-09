import pygame

from scripts.physics_entity import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "protagonist", pos, size)
        self.air_time = 0
        self.void_time = 0
        self.jumps = 1

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        if not (
            self.collisions["up"]
            or self.collisions["right"]
            or self.collisions["left"]
            or self.collisions["down"]
        ):
            self.void_time += 1
        else:
            self.void_time = 0

        # if self.void_time > 180:
        #     self.game.dead += 1
        # screenshake to add

        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0

        if self.air_time > 5:
            self.jumps = 0

        if self.air_time > 4:
            self.set_action("jump")
        elif movement[0] != 0:
            self.set_action("walk")
        else:
            self.set_action("idle")

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        else:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
