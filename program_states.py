from abc import ABC, abstractmethod

import pygame

vec = pygame.math.Vector2


class AbstractState(ABC):
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        self.og_screen_size = vec(317, 236)
        self.screen_scaling_factor = 3

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def change_res(self, new_screen_size, new_scaling):
        self.og_screen_size = new_screen_size
        self.screen_scaling_factor = new_scaling

