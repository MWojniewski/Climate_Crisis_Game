import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.anim_offset = (-4, -2)
        self.flip = False
        self.set_action("idle")

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.collisions["right"] = True
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    self.collisions["left"] = True
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        print(entity_rect.bottomleft, entity_rect.bottomright)
        for rect in tilemap.physics_rect_around(self.pos):
            print(rect.topleft, rect.topright)
            print()
            if entity_rect.colliderect(rect):
                print("collision")
                print()
                if frame_movement[1] > 0:
                    self.collisions["down"] = True
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.collisions["up"] = True
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):

        img = pygame.transform.flip(self.animation.img(), self.flip, False)

        render_x = self.pos[0] - offset[0] + self.anim_offset[0]
        render_y = self.pos[1] - offset[1] + self.anim_offset[1]

        mask = pygame.mask.from_surface(img)
        silhouette = mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))

        for mask_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            surf.blit(
                silhouette, (render_x + mask_offset[0], render_y + mask_offset[1])
            )

        surf.blit(img, (render_x, render_y))
