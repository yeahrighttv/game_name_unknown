import pygame
import config
from game import Game
from game_state import GameState
from player import index_advance

def main ():
    pygame.init()


screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption('Undertale Game')
icon = pygame.image.load('imgs/game_icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

game = Game(screen)
game.set_up()

time_elapsed = 0

while game.game_state == GameState.RUNNING:
    clock.tick()
    dt = clock.tick(30)
    game.update()
    pygame.display.flip()
    time_elapsed += dt
    #advance index every 200 milliseconds
    if time_elapsed > 200:
        index_advance()
        time_elapsed = 0



if __name__ == '__main__':
    main()

