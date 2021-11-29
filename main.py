import pygame
import config
from game import Game
from game_state import GameState

def main ():
    pygame.init()


screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption('Undertale Game')

game = Game(screen)
game.set_up()

while game.game_state == GameState.RUNNING:
    game.update()
    pygame.display.flip()

if __name__ == '__main__':
    main()