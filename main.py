import pygame, sys

pygame.init()

def main ():
    #start
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        pygame.display.flip()

if __name__ == '__main__':
    main()