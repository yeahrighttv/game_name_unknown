from functools import partial
from pygame.time import Clock

from camera import Camera, Follow, Border, Auto, Stand
from player import Player
from game_state import GameState
from program_states import RunningGame
from sprite import Sprite
import pygame
import config
vec = pygame.math.Vector2

NONE = GameState.NONE
RUNNING = GameState.RUNNING
ENDED = GameState.ENDED


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.og_screen_size = vec(317, 236)
        self.screen_scaling_factor = 3
        self.player = Player("imgs/player.png", 0, 0)

        self.game_state = RUNNING
        self.game_states = {
            RUNNING: RunningGame(self.screen, self, self.player)
        }

    def update(self):
        self.game_states.get(self.game_state).update()

    def change_state(self, new_state):
        self.game_state = new_state