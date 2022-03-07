from acts.test_act import TestAct
from program_states import AbstractState
from functools import partial

import pygame

import config
from camera import Camera, Follow, Border, Auto, Stand
from game_state import GameState
from running_game_hierarchy import Act
from sprite import Sprite, Hitbox

vec = pygame.math.Vector2


class RunningGame(AbstractState):
    def __init__(self, screen, game, player):
        super().__init__(screen, game)

        # self.objects = []

        self.bg_surface = pygame.surface.Surface(self.og_screen_size)

        # Keys for directions
        self.dct_directions = {
            pygame.K_w: "up",
            pygame.K_UP: "up",
            pygame.K_s: "down",
            pygame.K_DOWN: "down",
            pygame.K_a: "left",
            pygame.K_LEFT: "left",
            pygame.K_d: "right",
            pygame.K_RIGHT: "right",
        }

        self.player = player
        self.set_up()

    def set_up(self):

        # Camera setup
        self.camera = Camera(self.player, self.og_screen_size * self.screen_scaling_factor)
        self.camera.add_mode("follow", Follow(self.camera, self.player))
        self.camera.add_mode("border", Border(self.camera, self.player))
        self.camera.add_mode("auto", Auto(self.camera, self.player))
        self.camera.add_mode("stand", Stand(self.camera, self.player))

        self.camera.set_method("stand")

        # Keys to choose camera modes
        self.dct_camera_modes = {
            pygame.K_1: partial(self.camera.set_method, "border"),
            pygame.K_2: partial(self.camera.set_method, "follow"),
            pygame.K_3: partial(self.camera.set_method, "stand"),
            pygame.K_4: partial(self.camera.set_method, "auto"),
        }

        self.test_dct = {
            pygame.K_9: lambda x, y: self.game.change_resD(x, y - 1),
            pygame.K_0: lambda x, y: self.game.change_resI(x, y + 1),
            pygame.K_7: lambda x, y: self.game.change_state(GameState.MENU),
            pygame.K_o: lambda x, y: self.get_act().change_cur_scene("scene 1"),
            pygame.K_p: lambda x, y: self.get_act().change_cur_scene("scene 2"),
            pygame.K_k: lambda x, y: self.player.change_speed(200),
            pygame.K_l: lambda x, y: self.player.change_speed(2000),
        }

        self.act = "act 1"
        self.acts = {
            "act 1": TestAct(self.screen, self.game, self.player, self.camera, self),
        }

        # print('do set up')

    def get_act(self):
        return self.acts.get(self.act)

    # Moves and offsets camera
    def move_camera(self):
        self.camera.scroll()

    def render(self, bg_surface):
        self.screen.fill(config.BLACK)
        self.bg_surface.fill(config.BLACK)
        self.get_act().render(self.bg_surface)

        pygame.transform.scale(self.bg_surface, self.og_screen_size * self.screen_scaling_factor, dest_surface=self.screen)

    def update(self, dt):
        self.dt = dt
        # print('update')
        self.handle_events()
        self.player_movement(dt)
        self.move_camera()
        self.get_act().update(dt)
        self.render(None)

    """ SOMETIMES DOESN'T WORK WHEN MULTIPLE KEYS ARE PRESSED, SEEMS TO BE PYGAME BUG"""
    def player_movement(self, dt):
        pressed = pygame.key.get_pressed()
        # print(pressed[pygame.K_w],
        #       # pressed[pygame.K_UP],
        #       pressed[pygame.K_s],
        #       # pressed[pygame.K_DOWN],
        #       pressed[pygame.K_a],
        #       # pressed[pygame.K_LEFT],
        #       pressed[pygame.K_d],)
        #       # pressed[pygame.K_RIGHT])

        # Directions to int values
        up = int(pressed[pygame.K_w] or pressed[pygame.K_UP])
        down = int(pressed[pygame.K_s] or pressed[pygame.K_DOWN])
        left = int(pressed[pygame.K_a] or pressed[pygame.K_LEFT])
        right = int(pressed[pygame.K_d] or pressed[pygame.K_RIGHT])

        # Final horizontal and vertical directions
        hor = right - left
        ver = down - up

        # print(up, down, left, right, ver, hor)

        self.player.move(hor, ver, dt)

    # Handle things
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.change_state(GameState.ENDED)

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.ENDED)

                # Changes camera mode, if other keys defaults to empty lambda
                self.dct_camera_modes.get(event.key, lambda: None)()
                self.test_dct.get(event.key, lambda x, y: None)(self.og_screen_size, self.screen_scaling_factor)

            # Check if key is released
            elif event.type == pygame.KEYUP:
                pass
