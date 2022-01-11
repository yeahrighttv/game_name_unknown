import pygame
import config


class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.x = float(x)
        self.y = float(y)

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        # self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        # self.rect = pygame.Rect(self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE)

    # Renders sprite
    def render(self, surface, offset):
        surface.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))
