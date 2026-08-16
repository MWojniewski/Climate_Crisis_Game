import pygame
import json

LVL_NPCS = {0: (0,)}
NPC_NAME = [
    "cave_computer",  # 0
    "cave_rope",  # 1
]


class NPC:
    def __init__(self, game, npc_name, pos):
        self.game = game
        self.pos = pos
        self.name = npc_name

        self.active_npc = True
        self.in_x_range = False

        npc_file = open("data/npcs/" + self.name + ".json", "r")
        npc_data = json.load(npc_file)
        npc_file.close()

        self.states_list = npc_data["states_list"]
        self.state = 0
        self.interaction_text = npc_data["interaction_text"]
        self.text = npc_data["text"]
        self.x_area = []
        for pos_data in npc_data["x_area"]:
            self.x_area.append(
                pygame.Rect(
                    self.pos[0] + pos_data[0],
                    self.pos[1] + pos_data[1],
                    pos_data[2],
                    pos_data[3],
                )
            )
        self.animation = self.game.assets[
            "npcs/" + self.name + "/" + self.states_list[self.state]
        ].copy()

    def check_x_area(self, player_rect, player_pos, flip):
        for rect in self.x_area:
            if player_rect.colliderect(rect):
                if player_pos[0] - self.pos[0] > 0 and flip:
                    return True
                if player_pos[0] - self.pos[0] < 0 and not flip:
                    return True

    def update(self, display, offset=(0, 0)):
        self.animation.update()
        display.blit(
            self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1])
        )

    def interaction(self):
        self.state = (self.state + 1) % len(self.states_list)
        self.animation = self.game.assets[
            "npcs/" + self.name + "/" + self.states_list[self.state]
        ].copy()

    def draw_interaction_box(self, surf):

        x_key_img = self.game.assets["x_key"]
        text_str = self.interaction_text
        text_surf = self.game.interaction_font.render(text_str, False, (0, 0, 0))

        padding_x = 5
        padding_y = 3
        gap = 4

        box_width = padding_x * 2 + x_key_img.get_width() + gap + text_surf.get_width()
        box_height = padding_y * 2 + max(x_key_img.get_height(), text_surf.get_height())

        box_x = (self.game.GAME_WIDTH - box_width) // 2
        box_y = self.game.GAME_HEIGHT - box_height - 10

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        pygame.draw.rect(surf, (192, 192, 192), box_rect)

        pygame.draw.rect(surf, (0, 0, 0), box_rect, 1)

        icon_y = box_y + (box_height - x_key_img.get_height()) // 2
        text_y = box_y + (box_height - text_surf.get_height()) // 2

        icon_x = box_x + padding_x
        surf.blit(x_key_img, (icon_x, icon_y))

        text_x = icon_x + x_key_img.get_width() + gap
        surf.blit(text_surf, (text_x, text_y))
