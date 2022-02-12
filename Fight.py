import random

import pygame

import config
from game_state import GameState
from program_states import AbstractState
from sprite import Sprite, NPC, Sans, DialogBox, DialogOption

vec = pygame.math.Vector2


class Fight(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)
        self.bg_surface = pygame.surface.Surface(self.og_screen_size)

        self.player = player
        self.npc = None
        self.dialog_box = DialogBox()

        self.option = None
        self.options = [
            DialogOption("imgs/rock.png", x=14, y=216),
            DialogOption("imgs/paper.png", x=114, y=216),
            DialogOption("imgs/scissors.png", x=213, y=216),
        ]
        self.option_images = [
            DialogOption("imgs/rock_outside_box.png", x=60, y=168),
            DialogOption("imgs/paper_outside_box.png", x=60, y=168),
            DialogOption("imgs/scissors_outside_box.png", x=60, y=168),
        ]

        self.npc_option = None
        self.npc_options = [
            DialogOption("imgs/rock_outside_box.png", x=240, y=168),
            DialogOption("imgs/paper_outside_box.png", x=240, y=168),
            DialogOption("imgs/scissors_outside_box.png", x=240, y=168),
        ]

        self.time_until_cooldown = 0
        self.time_until_secondary_cooldown = 0
        self.cooldown = 5000
        self.secondary_cooldown = 150

        self.set_up()

    def change_npc(self, npc):
        self.npc = npc

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
        }

    def render_chosen_options(self, surface):
        if self.option is not None:
            self.option_images[self.option].render(surface, self.dt)

        if self.npc_option is not None:
            self.npc_options[self.npc_option].render(surface, self.dt)

    def render(self, bg_surface=None):
        self.bg_surface.fill(config.BLACK)
        self.npc.render_fight(self.bg_surface, self.dt)
        self.dialog_box.render(self.bg_surface)

        self.render_chosen_options(self.bg_surface)

        for option in self.options:
            option.render(self.bg_surface, self.dt)

        pygame.transform.scale(self.bg_surface, self.og_screen_size * self.screen_scaling_factor,
                               dest_surface=self.screen)

    def update(self, dt):
        self.dt = dt
        self.check_mouse_events()
        self.handle_events()
        self.render()
        self.cooldown_method()

    def cooldown_method(self):
        self.time_until_cooldown -= self.dt
        self.time_until_secondary_cooldown -= self.dt

        if self.time_until_cooldown > self.cooldown - 2000:
            if self.time_until_secondary_cooldown <= 0:
                self.npc_choice()
                self.time_until_secondary_cooldown = self.secondary_cooldown

    def npc_choice(self):
        self.npc_option = random.randint(0, 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.time_until_cooldown <= 0:
                    for i, option in enumerate(self.options):
                        if option.moused_over:
                            self.time_until_cooldown = self.cooldown
                            self.option = i
                            break

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.ENDED)

                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)

            # Check if key is released
            elif event.type == pygame.KEYUP:
                pass

    def check_mouse_events(self):
        for option in self.options:
            option.moused_over = False
            if option.rect.collidepoint(pygame.mouse.get_pos()[0] / 3, pygame.mouse.get_pos()[1] / 3):
                option.moused_over = True
