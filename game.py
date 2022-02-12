from menu import Menu
from player import Player
from game_state import GameState
import pygame

from running_game import RunningGame

vec = pygame.math.Vector2

NONE = GameState.NONE
RUNNING = GameState.RUNNING
ENDED = GameState.ENDED
MENU = GameState.MENU


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player("imgs/player.png", 0, 0, center=True)

        self.game_state = RUNNING
        self.game_states = {
            RUNNING: RunningGame(self.screen, self, self.player),
            MENU: Menu(self.screen, self)

        }
        self.current_state_obj = self.game_states.get(self.game_state)
        self.dt = 0

    def update(self, dt):
        self.dt = dt
        self.current_state_obj.update(dt)

    def change_state(self, new_state):
        self.game_state = new_state
        self.current_state_obj = self.game_states.get(self.game_state)

    def change_res(self, new_res, new_scaling):
        pygame.display.set_mode(new_res * new_scaling)
        self.current_state_obj.change_res(new_res, new_scaling)
