import math
import random

import pygame
import config

vec = pygame.math.Vector2

class Hitbox(pygame.Rect):
    def __init__(self, surface, x, y, width, height):
        self.Hitbox = pygame.Rect(surface, x, y, width, height)
    
    def render(self, surface, offset, dt):
        surface.blit(self.Hitbox, (self.rect.x - offset.x, self.rect.y - offset.y))

