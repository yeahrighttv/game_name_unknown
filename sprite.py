import math

import pygame
import config


class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, x=0, y=0, center=False):
        self.path = path
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
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


class SpriteInsideHouse(Sprite):
    def __init__(self, path, x=0, y=0, center=False):
        super().__init__(path, x, y, center)

    def center(self):
        self.rect.update(self.rect.x + 2 + (-self.rect.w / 2),
                         self.rect.y + 2 + (-self.rect.h / 2),
                         self.rect.w,
                         self.rect.h)
