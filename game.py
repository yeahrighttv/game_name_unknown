import pygame
from player import Player
import config
from game_state import GameState

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print('do set up')
        self.game_state = GameState.RUNNING

#        self.

    def update(self):
        self.screen.fill(config.BLACK)
        print('update')
        self.handle_events()

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # hanlde key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w or event.key == pygame.K_UP: # up
                    self.player.update_position(0, -1)
                    print("up")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # down
                    self.player.update_position(0, 1)
                    print("down")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # left
                    self.player.update_position(-1, 0)
                    print("left")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # right
                    self.player.update_position(1, 0)
                    print("right")
