import pygame, sys
from pygame.locals import *

def main ():
    pygame.init()

    screen = pygame.display.set_mode(500, 500)
    pygame.display.set_caption('Gyarbete')

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


if __name__ == '__main__':
    main()