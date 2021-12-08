import pygame
import config
from game import Game
from game_state import GameState
from player import index_advance

def main ():
    pygame.init()

screen = pygame.display.set_mode((317 * 2, 236 * 2))
pygame.display.set_caption('Undertale Game')
icon = pygame.image.load('imgs/game_icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

game = Game(screen)
game.set_up()

time_elapsed = 0

while game.game_state == GameState.RUNNING:
    clock.tick()
    dt = clock.tick(90)
    game.update()
    pygame.display.flip()
    time_elapsed += dt
    #advance index every 90 milliseconds
    if time_elapsed > 90:
        index_advance()
        time_elapsed = 0



if __name__ == '__main__':
    main()

