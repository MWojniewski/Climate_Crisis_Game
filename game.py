import pygame
import sys
from scripts.physics_entity import PhysicsEntity
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, load_image_alpha, Animation
from scripts.npc import LVL_NPCS, NPC_NAME, NPC


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Climate Crisis Game")
        pygame.font.init()

        self.GAME_WIDTH = 320
        self.GAME_HEIGHT = 180

        self.screen = pygame.display.set_mode(
            (self.GAME_WIDTH, self.GAME_HEIGHT), pygame.FULLSCREEN | pygame.SCALED
        )

        self.display = pygame.Surface(
            (self.GAME_WIDTH, self.GAME_HEIGHT), pygame.SRCALPHA
        )
        self.display_2 = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.interaction_font = pygame.font.Font("data/fonts/PixeloidMono.ttf", 9)

        self.movement = [False, False]

        self.assets = {
            "diode_metal": load_images("tiles/diode_metal"),
            "metal": load_images("tiles/metal"),
            "large_decor": load_images("tiles/large_decor"),
            "protagonist": load_image("entities/protagonist.png"),
            "background": load_image("backgrounds/background.png"),
            "x_key": load_image_alpha("x_key.png"),
            "protagonist/idle": Animation(
                load_images("entities/protagonist/idle"), img_dur=20
            ),
            "protagonist/walk": Animation(
                load_images("entities/protagonist/walk"), img_dur=2
            ),
            "protagonist/jump": Animation(load_images("entities/protagonist/jump")),
            "npcs/cave_computer/off": Animation(
                load_images("npcs/cave_computer/off"), img_dur=30
            ),
            "npcs/cave_computer/on": Animation(
                load_images("npcs/cave_computer/on"), img_dur=30
            ),
        }

        self.player = Player(self, (150, 50), (19, 30))
        self.tilemap = Tilemap(self, tile_size=16)
        self.level = 0
        self.lvl_npc = []
        self.npc_in_range = -1

        self.load_level()

    def load_level(self):
        self.lvl_npc = []
        self.tilemap.load("data/maps/edited_map.json")

        for spawner in self.tilemap.extract([("spawners", 0)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]

        npc_temp_list = []

        for npc_number in LVL_NPCS[self.level]:
            npc_temp_list.append(("npcs", npc_number))
        for npc in self.tilemap.extract(npc_temp_list):
            self.lvl_npc.append(NPC(self, NPC_NAME[npc["variant"]], npc["pos"]))

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
                - 15
            ) / 30
            self.render_scroll = (round(self.scroll[0]), round(self.scroll[1]))

            self.tilemap.render(self.display, offset=self.render_scroll)

            for npc in self.lvl_npc:
                npc.update(self.display, offset=self.render_scroll)

            display_mask = pygame.mask.from_surface(self.display)
            display_silhouette = display_mask.to_surface(
                setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0)
            )
            for offset in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                self.display_2.blit(display_silhouette, offset)

            self.display_2.blit(self.display, (0, 0))

            # if not self.dead:
            self.player.update(
                self.tilemap, (1.3 * (self.movement[1] - self.movement[0]), 0)
            )
            self.player.render(self.display_2, offset=self.render_scroll)

            if self.player.collisions["down"] and not self.player.jumps:
                self.player.jumps += 1

            self.npc_in_range = -1
            if self.player.jumps:
                for index, npc in enumerate(self.lvl_npc):
                    if npc.active_npc and npc.check_x_area(
                        self.player.rect(), self.player.pos, self.player.flip
                    ):
                        self.npc_in_range = index
                        npc.draw_interaction_box(self.display_2)
                        break

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
                            pass
                            # self.sfx["jump"].play()
                    if event.key == pygame.K_x and not self.npc_in_range == -1:
                        self.lvl_npc[self.npc_in_range].interaction(self.display_2)

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
