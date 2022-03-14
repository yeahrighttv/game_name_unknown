import pygame
from acts.test_act import TestHouse
import config
from game import Game
from game_state import GameState


def main():
    screen = pygame.display.set_mode((317 * 3, 236 * 3))
    game = Game(screen)

    pygame.display.set_caption('Game Name Unkown')
    icon = pygame.image.load('imgs/game_icon.png')
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    time_elapsed = 0

    while game.game_state != GameState.ENDED:
        """ NEED TO MAKE SPEED FRAME RATE INDEPENDENT"""
        dt = clock.tick(144)
        game.update(dt)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
