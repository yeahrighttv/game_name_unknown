import textboxify
import pygame
import numpy
import config

from game_state import GameState
from program_states import AbstractState
from sprite import NPC
from textboxify.borders import DEFAULT
from textboxify.util import load_image

vec = pygame.math.Vector2


class Dialogue(AbstractState):
    def __init__(self, screen, game):
        super().__init__(screen, game)

        #self.dialogue_text = dialogue_text

        screen_size = self.og_screen_size * self.screen_scaling_factor

        #portrait = main_fight_sprite_path.get_rect()
        #portrait_width = int(portrait.x)
        #portrait_height = int(portrait.y)

        dialog_box = textboxify.TextBoxFrame(
            text='hi',
            text_width=(screen_size.x // 2),
            lines=2,
            pos=((screen_size.x // 8), (screen_size.y // 2)),
            padding=(150, 100),
            font_color=(255, 255, 255),
            font_size=26,
            bg_color=(0, 0, 0),
            border=DEFAULT,
            alpha=255
        )

#        draw_group = pygame.sprite.LayeredDirty()
#        draw_group.clear(screen)

        dialog_box.set_indicator()

        #dialog_box.set_portrait(f"imgs/{main_fight_sprite_path}", (portrait_width, portrait_height))

    def start(self, npc, from_object):
        pass

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_Q: lambda s, y: self.game.change_state(GameState.RUNNING)
        }

    def render(self):
        self.screen.fill(config.WHITE)

    def update(self, dt):
        self.render()
        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.ENDED)
