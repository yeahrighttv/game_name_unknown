import pygame

import config
from game_state import GameState
from program_states import AbstractState

NONE = GameState.NONE
RUNNING = GameState.RUNNING
ENDED = GameState.ENDED
MENU = GameState.MENU


class Menu(AbstractState):
    def __init__(self, screen, game):
        super().__init__(screen, game)

        self.set_up()

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(RUNNING),
        }

    def render(self):
        self.screen.fill(config.WHITE)
        pygame.transform.scale(self.screen, self.og_screen_size * self.screen_scaling_factor)

    def update(self):
        self.handle_events()
        self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(ENDED)

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(ENDED)

                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)


            # Check if key is released
            elif event.type == pygame.KEYUP:
                pass