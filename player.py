import pygame
import config

class Player:
    def __init__(self):
        print('Player Created')

    def update(self):
        print('Player Updated')

    def render(self, screen):
        screen.draw.rect(screen, config.WHITE, (10, 10, 10, 10), 4)