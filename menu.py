import pygame

import config
from game_state import GameState
from program_states import AbstractState


class Menu(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)

        self.player = player
        self.menu = pygame.image.load('imgs/Assets/menu.png')
        self.menu_rect = self.menu.get_rect()
        self.menu_rect.center = (150 * .85, (236 * 3) * .4)
        # Set the cursor and menu states
        self.menu_options = {0: 'Items', 1: 'Exit'}
        self.index = 0
        # Variables for the cursor
        self.cursor = pygame.image.load('imgs/Assets/cursor.png')
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_posy = self.menu_rect.y + 98
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_posy
        self.set_up()

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render(self):
        self.screen.blit(self.menu, self.menu_rect)
        self.screen.blit(self.cursor, self.cursor_rect)
        pygame.transform.scale(self.screen, self.og_screen_size * self.screen_scaling_factor)

    def update(self, dt):
        self.update_cursor()
        self.handle_events()
        self.render()

    def update_cursor(self):
        # This updates the cursor
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.menu_options)
                elif event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.index] == 'Items':
                        self.screen.fill(config.WHITE)
                    elif self.menu_options[self.index] == 'Exit':
                        self.index = 0
                        self.game.change_state(GameState.RUNNING)
                self.cursor_rect.y = self.cursor_posy + (self.index * 30)

            elif event.type == pygame.KEYUP:
                pass

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
