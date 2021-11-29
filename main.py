import pygame
import config
from game import Game
from game_state import GameState

def main ():
    pygame.init()


screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Undertale Game')

clock = pygame.time.Clock()

game = Game(screen)
game.set_up()

while game.game_state == GameState.RUNNING:
    clock.tick(50)
    game.update()
    pygame.display.flip()



if __name__ == '__main__':
    main()