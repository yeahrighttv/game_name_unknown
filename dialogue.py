import textboxify
import pygame
import numpy
import config

from game_state import GameState
from program_states import AbstractState
from sprite import Neutral, TestNPC
from textboxify.borders import DEFAULT
from textboxify.util import load_image

vec = pygame.math.Vector2


class Dialogue(AbstractState):
    def __init__(self, screen, game):
        super().__init__(screen, game)

        #self.dialogue_text = dialogue_text

        screen_size = self.og_screen_size * self.screen_scaling_factor

        self.dialog_box = textboxify.TextBoxFrame(
            text='What the fuck did you just fucking say about me, you little bitch?',
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

        self.draw_group = pygame.sprite.LayeredDirty()
#        draw_group.clear(screen)

        self.dialog_box.set_indicator()

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
        if not self.draw_group:
            self.draw_group.add(self.dialog_box)
        self.dialog_box.update()

    def update(self, dt):
        self.render()
        self.handle_events()
        self.draw_group.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.ENDED)
                if event.key == pygame.K_RETURN:
                    if self.dialog_box.words:
                        self.dialog_box.reset()
                    else:
                        self.dialog_box.reset(hard=True)
                        self.dialog_box.set_text("this is just bugged now, byebye")
                        self.dialog_box.kill()
