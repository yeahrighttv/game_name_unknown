import pygame
import config
from game import Game

def main ():
    pygame.init()


screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Undertale Game')

game = Game(screen)
game.set_up()

while True:
    game.update()
    pygame.display.flip()

if __name__ == '__main__':
    main()