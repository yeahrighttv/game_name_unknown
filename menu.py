import pygame

import config
from game_state import GameState
from program_states import AbstractState
from sprite import DialogBox


class Menu(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)

        self.player = player

        screen_size = self.og_screen_size * self.screen_scaling_factor

        # Inventory box
        self.inventory_box = DialogBox('imgs/inventory_box.png')
        self.inventory_box.rect.x = screen_size.x // 2 - self.inventory_box.rect.w // 2
        self.inventory_box.rect.y = screen_size.y // 2 - self.inventory_box.rect.h // 2

        self.menu = pygame.image.load('imgs/Assets/menu.png')
        self.menu_rect = self.menu.get_rect()
        self.menu_rect.x = self.inventory_box.rect.x - 110
        self.menu_rect.y = self.inventory_box.rect.y + self.inventory_box.rect.h - self.menu_rect.h

        # Set the cursor and menu states
        self.menu_options = {0: 'Items', 1: 'Exit'}
        self.index = 0

        # Variables for the cursor
        self.cursor = pygame.image.load('imgs/Assets/cursor.png')
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_posy = self.menu_rect.y + 98
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_posy

        self.show_items = False

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

        if self.show_items:
            self.inventory_box.render(self.screen)
            self.player.inventory.render_inventory()

        pygame.transform.scale(self.screen, self.og_screen_size * self.screen_scaling_factor)

    def update(self, dt):
        self.handle_events()
        self.render()

    def update_cursor(self, event):
        # This updates the cursor
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.index = (self.index + 1) % len(self.menu_options)
            elif event.key == pygame.K_UP:
                self.index = (self.index - 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.menu_options[self.index] == 'Items':
                    self.show_items = True
                elif self.menu_options[self.index] == 'Exit':
                    self.show_items = False
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

            self.update_cursor(event)
