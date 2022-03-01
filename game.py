from Fight import Fight
from menu import Menu
from player import Player
from game_state import GameState
import pygame

from running_game import RunningGame

vec = pygame.math.Vector2



class Game:
    def __init__(self, screen):
        self.volume = 1
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

        self.screen = screen
        self.player = Player("imgs/player.png", 0, 0, center=True)

        self.game_state = GameState.RUNNING
        self.game_states = {
            GameState.RUNNING: RunningGame(self.screen, self, self.player),
            GameState.MENU: Menu(self.screen, self),
            GameState.FIGHT: Fight(self.screen, self, self.player, )
        }
        self.current_state_obj = self.game_states.get(self.game_state)
        self.dt = 0
        self.resolution_factor = 0

    def update(self, dt):
        self.dt = dt
        self.current_state_obj.update(dt)

    def change_state(self, new_state):
        self.game_state = new_state
        self.current_state_obj = self.game_states.get(self.game_state)


    def change_resI(self, new_res, new_scaling):
        self.resolution_factor += 1
        print(self.resolution_factor)
        pygame.display.set_mode(new_res * new_scaling)
        self.current_state_obj.change_res(new_res, new_scaling)

    def change_resD(self, new_res, new_scaling):

        if self.resolution_factor >= -1:
            pygame.display.set_mode(new_res * new_scaling)
            self.current_state_obj.change_res(new_res, new_scaling)

        if self.resolution_factor >= -1:
            self.resolution_factor -= 1
        print(self.resolution_factor)
        
