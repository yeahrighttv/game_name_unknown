from functools import partial
from pygame.time import Clock

from camera import Camera, Follow, Border, Auto, Stand
from player import Player
from game_state import GameState
from sprite import Sprite
import pygame
import config
vec = pygame.math.Vector2


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.og_screen_size = vec(317, 236)
        self.screen_scaling_factor = 3
        self.bgsurface = pygame.surface.Surface(self.og_screen_size)
        self.game_state = GameState.NONE

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

    # Temp scene fix
    def add_kitchen_objects(self):
        self.objects.append(Sprite("imgs/Staircase_1.png"))
        self.objects.append(Sprite("imgs/Room_Entrance.png"))
        self.objects.append(self.player)
        self.objects.append(Sprite("imgs/Railing_asset1.png"))
        self.objects.append(Sprite("imgs/Railing_asset2.png"))
        self.objects.append(Sprite("imgs/Railing_asset3.png"))

        # Centering objects
        for object in self.objects:
            object.center()

    def add_snowdin_objects(self):
        self.objects.append(Sprite("imgs/snowdin.png"))
        self.objects.append(self.player)

        # Centering objects
        for object in self.objects:
            object.center()

    def add_zelda_objects(self):
        self.objects.append(Sprite("imgs/zelda_map_test.png"))
        self.objects.append(self.player)

        # Centering objects
        for object in self.objects:
            object.center()

    def set_up(self):
        self.player = Player("imgs/player.png", 0, 0)

        # Camera setup
        self.camera = Camera(self.player, self.og_screen_size * self.screen_scaling_factor)
        self.camera.add_mode("follow", Follow(self.camera, self.player))
        self.camera.add_mode("border", Border(self.camera, self.player))
        self.camera.add_mode("auto", Auto(self.camera, self.player))
        self.camera.add_mode("stand", Stand(self.camera, self.player))

        # self.camera.set_method("follow")
        # self.camera.set_method("border")
        # self.camera.set_method("auto")
        self.camera.set_method("stand")

        # Keys to choose camera modes
        self.dct_camera_modes = {
            pygame.K_1: partial(self.camera.set_method, "border"),
            pygame.K_2: partial(self.camera.set_method, "follow"),
            pygame.K_3: partial(self.camera.set_method, "stand"),
            pygame.K_4: partial(self.camera.set_method, "auto"),
        }


        # Kitchen scene
        self.add_kitchen_objects()

        # Snowdin scene
        # self.add_snowdin_objects()

        # Zelda map test
        # self.add_zelda_objects()


        print('do set up')
        self.game_state = GameState.RUNNING

    # Moves and offsets camera
    def move_camera(self):
        self.camera.scroll()

    def render(self):
        self.screen.fill(config.BLACK)
        self.bgsurface.fill(config.BLACK)

        for object in self.objects:
            object.render(self.bgsurface, self.camera.offset)

        pygame.transform.scale(self.bgsurface, self.og_screen_size * self.screen_scaling_factor, dest_surface=self.screen)

    def update(self):
        # print('update')
        self.handle_events()
        self.player_movement()
        self.move_camera()
        self.render()

    def player_movement(self):
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

        self.player.move(hor, ver)

    # Handle things
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED

            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED

                # Changes camera mode, if other keys defaults to empty lambda
                self.dct_camera_modes.get(event.key, lambda: None)()

            # Check if key is released
            elif event.type == pygame.KEYUP:
                pass
