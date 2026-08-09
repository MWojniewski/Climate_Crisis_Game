import pygame
import sys
from scripts.physics_entity import PhysicsEntity
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, load_image_alpha, Animation


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Climate Crisis Game")

        self.GAME_WIDTH = 640
        self.GAME_HEIGHT = 360

        self.screen = pygame.display.set_mode(
            (self.GAME_WIDTH, self.GAME_HEIGHT), pygame.FULLSCREEN | pygame.SCALED
        )

        self.display = pygame.Surface(
            (self.GAME_WIDTH, self.GAME_HEIGHT), pygame.SRCALPHA
        )
        self.display_2 = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "diode_metal": load_images("tiles/diode_metal"),
            "metal": load_images("tiles/metal"),
            "large_decor": load_images("tiles/large_decor"),
            "protagonist": load_image("entities/protagonist.png"),
            "background": load_image("backgrounds/background.png"),
            "protagonist/idle": Animation(
                load_images("entities/protagonist/idle"), img_dur=20
            ),
            "protagonist/walk": Animation(
                load_images("entities/protagonist/walk"), img_dur=4
            ),
            "protagonist/jump": Animation(load_images("entities/protagonist/jump")),
        }

        self.player = Player(self, (150, 50), (19, 30))
        self.tilemap = Tilemap(self, tile_size=16)

        self.load_level()

    def load_level(self):
        self.tilemap.load("data/maps/edited_map.json")

        self.scroll = [0, 0]
        self.transition = -45

    def run(self):
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets["background"], (0, 0))

            # self.screen_shake = max(0, self.screen_shake - 1)

            if self.transition < 0:
                self.transition += 1

            # if self.dead:
            #     self.dead += 1
            #     if self.dead >= 10:
            #         self.transition = min(self.transition + 1, 30)
            #     if self.dead > 40:
            #         self.load_level(self.level)

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=self.render_scroll)

            display_mask = pygame.mask.from_surface(self.display)
            display_silhouette = display_mask.to_surface(
                setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0)
            )
            for offset in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                self.display_2.blit(display_silhouette, offset)

            self.display_2.blit(self.display, (0, 0))

            # if not self.dead:
            self.player.update(
                self.tilemap, (1.5 * (self.movement[1] - self.movement[0]), 0)
            )
            self.player.render(self.display_2, offset=self.render_scroll)

            if self.player.collisions["down"] and not self.player.jumps:
                self.player.jumps += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            print("jump")
                            # self.sfx["jump"].play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition:
                transition_surf = pygame.Surface(self.display_2.get_size())
                pygame.draw.circle(
                    transition_surf,
                    (255, 255, 255),
                    (self.display_2.get_width() // 2, self.display_2.get_height() // 2),
                    (45 - abs(self.transition)) * 8,
                )
                transition_surf.set_colorkey((255, 255, 255))
                self.display_2.blit(transition_surf, (0, 0))

            # screenshake_offset = (
            #     random.random() * self.screen_shake - self.screen_shake / 2,
            #     random.random() * self.screen_shake - self.screen_shake / 2,
            # )
            # self.changed_surf = pygame.transform.scale(self.display_2, (640, 480))
            self.screen.blit(self.display_2, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            # print(self.player.air_time)


Game().run()
