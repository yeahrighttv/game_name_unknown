from abc import ABC, abstractmethod

import pygame

vec = pygame.math.Vector2


class AbstractState(ABC):
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        self.og_screen_size = vec(317, 236)
        self.screen_scaling_factor = 3
        self.dt = 0

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def render(self, bg_surface):
        pass

    @abstractmethod
    def update(self, dt):
        self.dt = dt

    def change_res(self, new_res, new_scaling):
        self.og_screen_size = new_res
        self.screen_scaling_factor = new_scaling
