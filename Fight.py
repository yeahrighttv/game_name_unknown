import pygame

import config
from game_state import GameState
from program_states import AbstractState
from sprite import Sprite, NPC, Sans, DialogBox

vec = pygame.math.Vector2


class Fight(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)
        self.player = player
        self.npc = None
        self.dialog_box = DialogBox()

        self.option = 0
        self.options = [
            DialogBox("imgs/rock.png", x=14, y=216),
            DialogBox("imgs/paper.png", x=114, y=216),
            DialogBox("imgs/scissors.png", x=213, y=216),
        ]

        self.set_up()

    def change_npc(self, npc):
        self.npc = npc

    def set_up(self):
        self.bg_surface = pygame.surface.Surface(self.og_screen_size)

        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render(self, bg_surface=None):
        self.bg_surface.fill(config.BLACK)
        self.npc.render_fight(self.bg_surface, self.dt)
        self.dialog_box.render(self.bg_surface)

        for option in self.options:
            option.render(self.bg_surface)

        pygame.transform.scale(self.bg_surface, self.og_screen_size * self.screen_scaling_factor,
                               dest_surface=self.screen)

    def update(self, dt):
        self.dt = dt
        self.render()
        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.ENDED)

                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)

            # Check if key is released
            elif event.type == pygame.KEYUP:
                pass
