from functools import partial
from pygame.time import Clock
from player import Player
from game_state import GameState
from sprite import Sprite
import pygame
import config


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.bgsurface = pygame.surface.Surface((317, 236))
        self.game_state = GameState.NONE

    def set_up(self):
        self.player = Player("imgs/player.png", 4.5, 6.4)

        self.objects.append(Sprite("imgs/Staircase_1.png"))
        self.objects.append(Sprite("imgs/Room_Entrance.png"))
        self.objects.append(self.player)
        self.objects.append(Sprite("imgs/Railing_asset1.png"))
        self.objects.append(Sprite("imgs/Railing_asset2.png"))
        self.objects.append(Sprite("imgs/Railing_asset3.png"))

        print('do set up')
        self.game_state = GameState.RUNNING

    def render(self):
        self.screen.fill(config.BLACK)
        self.bgsurface.fill(config.BLACK)

        for object in self.objects:
            object.render(self.bgsurface)

        pygame.transform.scale(self.bgsurface, (317 * 3, 236 * 3), dest_surface=self.screen)

    # Update (loops)
    def update(self):
        # print('update')
        self.handle_events()
        self.player.update_position()
        self.render()

    # Player movement
    def player_movement(self):
        pressed = pygame.key.get_pressed()
        self.player.up_pressed = pressed[pygame.K_w] or pressed[pygame.K_UP]
        self.player.down_pressed = pressed[pygame.K_s] or pressed[pygame.K_DOWN]
        self.player.left_pressed = pressed[pygame.K_a] or pressed[pygame.K_LEFT]
        self.player.right_pressed = pressed[pygame.K_d] or pressed[pygame.K_RIGHT]

    # Handle things
    def handle_events(self):
        self.player_movement()

        for event in pygame.event.get():
            dct = {
                pygame.K_w: "up",
                pygame.K_UP: "up",
                pygame.K_s: "down",
                pygame.K_DOWN: "down",
                pygame.K_a: "left",
                pygame.K_LEFT: "left",
                pygame.K_d: "right",
                pygame.K_RIGHT: "right",
            }

            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED

            # Handle key events
            # Check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED

                self.player.direction = dct.get(event.key)

            # Check if key is released and re-falsify booleans
            elif event.type == pygame.KEYUP:
                pass
