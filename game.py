from player import Player
from game_state import GameState
import pygame

from running_game import RunningGame

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
        self.current_state_obj = self.game_states.get(self.game_state)

    def update(self):
        self.current_state_obj.update()

    def change_state(self, new_state):
        self.game_state = new_state

    def change_res(self, new_res, new_scaling):
        self.current_state_obj.change_res(new_res, new_scaling)
