import random
from itertools import cycle

import pygame

import config
from game_state import GameState
from program_states import AbstractState
from sprite import Sprite, NPC, Sans, DialogBox, DialogOption

vec = pygame.math.Vector2


class Fight(AbstractState):
    def __init__(self, screen, game, player):
        self.form_object = None

        self.click_sound = pygame.mixer.Sound("audio/click.wav")

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

        self.real_npc_option = None
        self.npc_option = None
        self.npc_options = [
            DialogOption("imgs/rock_outside_box.png", x=240, y=168),
            DialogOption("imgs/paper_outside_box.png", x=240, y=168),
            DialogOption("imgs/scissors_outside_box.png", x=240, y=168),
        ]
        self.possible_values = cycle([0, 1, 2])

        self.time_until_cooldown = 0
        self.time_until_secondary_cooldown = 0
        self.time_until_sound_cooldown = 0
        self.cooldown = 2100
        self.secondary_cooldown = 150
        self.sound_cooldown = 150

        self.can_attack = True

        self.set_up()

    def set_up(self):
        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_res(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_res(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.RUNNING),
            pygame.K_j: lambda x, y: self.npc.receive_damage(50),
        }

    def end(self):
        self.time_until_cooldown = 0
        self.time_until_secondary_cooldown = 0
        self.time_until_sound_cooldown = 0
        self.option = None
        self.npc_option = None

        self.player.rect.x, self.player.rect.y = self.npc.rect.x - self.player.rect.w, self.npc.rect.y
        self.game.change_state(GameState.RUNNING)
        self.click_sound.stop()
        self.form_object.play_music()

    def start(self, npc, from_object):
        self.form_object = from_object

        self.change_npc(npc)
        self.option = None
        self.npc_option = None
        self.npc.hp = self.npc.max_hp
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)

    def change_npc(self, npc):
        self.npc = npc
        pygame.mixer.music.load(self.npc.music_path)
        pygame.mixer.music.rewind()

    def find_winner(self):
        if self.option == 0:
            if self.npc_option == 2:
                self.npc.receive_damage(self.player.dmg)
        elif self.option == 1:
            if self.npc_option == 0:
                self.npc.receive_damage(self.player.dmg)
        elif self.option == 2:
            if self.npc_option == 1:
                self.npc.receive_damage(self.player.dmg)

    def check_if_npc_died(self):
        if self.npc.hp <= 0:
            self.end()

    def render_chosen_options(self, surface):
        if self.option is not None:
            self.option_images[self.option].render(surface, self.dt)

        if self.npc_option is not None:
            self.npc_options[self.npc_option].render(surface, self.dt)

    def render(self, bg_surface=None):
        self.bg_surface.fill(config.BLACK)
        self.npc.render_hp(self.bg_surface)
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
        self.check_if_npc_died()

    def cooldown_method(self):
        self.time_until_cooldown -= self.dt
        self.time_until_secondary_cooldown -= self.dt
        self.time_until_sound_cooldown -= self.dt

        if self.time_until_cooldown > self.cooldown - 2000:
            if self.time_until_secondary_cooldown <= 0:
                self.npc_choice()
                self.time_until_secondary_cooldown = self.secondary_cooldown
            if self.time_until_sound_cooldown <= 0:
                self.click_sound.play()
                self.time_until_sound_cooldown = self.sound_cooldown
        elif 0 < self.time_until_cooldown < self.cooldown - 2000:
            if self.can_attack:
                self.can_attack = False
                self.find_winner()
        elif self.time_until_cooldown <= 0:
            self.can_attack = True

    def npc_choice(self):
        if self.npc_option is None:
            self.npc_option = 0
        else:
            for _ in range(random.randint(1, 2)):
                self.npc_option = next(self.possible_values)

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
