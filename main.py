import pygame
import config
from game import Game
from game_state import GameState


def main():
    pygame.init()


screen = pygame.display.set_mode((317 * 3, 236 * 3))
pygame.display.set_caption('Undertale Game')
icon = pygame.image.load('imgs/game_icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

game = Game(screen)

time_elapsed = 0

while game.game_state != GameState.ENDED:
    """ NEED TO MAKE SPEED FRAME RATE INDEPENDENT"""
    dt = clock.tick(144)
    game.update()
    pygame.display.flip()
    time_elapsed += dt

    # Advance animation every 200 milliseconds
    if time_elapsed > 200:
        game.player.advance_animation()
        time_elapsed = 0


if __name__ == '__main__':
    main()
