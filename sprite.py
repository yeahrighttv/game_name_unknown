import pygame
import config


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        pygame.sprite.Sprite.__init__(self)
        self.x = float(x)
        self.y = float(y)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE)

    def render(self, surface):
        surface.blit(self.image, self.rect)
