import math

import pygame
import config

vec = pygame.math.Vector2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, x=0, y=0, center=False, scale=False):
        self.path = path
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        if scale:
            self.image = pygame.transform.scale(self.image, vec(317, 236))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

        if center:
            self.center()

    def render(self, surface, offset):
        surface.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

        # Collision box
        pygame.draw.rect(surface, config.RED, pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h), width=1)

    def center(self):
        self.rect.update(self.rect.x + (-self.rect.w / 2),
                         self.rect.y + (-self.rect.h / 2),
                         self.rect.w,
                         self.rect.h)
