import pygame

import config
from game_state import GameState
from program_states import AbstractState


class Fight(AbstractState):
    def __init__(self, screen, game):
        super().__init__(screen, game)

        self.set_up()

    def set_up(self):
        self.bg_surface = pygame.surface.Surface(self.og_screen_size)

        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render(self, bg_surface=None):
        self.bg_surface.fill(config.BLUE)

        pygame.transform.scale(self.bg_surface, self.og_screen_size * self.screen_scaling_factor,
                               dest_surface=self.screen)

    def update(self, dt):
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
