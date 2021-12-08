import pygame
from pygame.time import Clock
from player import Player, index_advance
import config
from game_state import GameState



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(4.5, 6.4)
        self.player = player
        self.objects.append(player)
        print('do set up')
        self.game_state = GameState.RUNNING

#        self.
    #update (loops)
    def update(self):
        self.screen.fill(config.BLACK)
        print('update')
        self.handle_events()
        self.player.update_position()
        print(self.player.x, self.player.y)
        for object in self.objects:
            object.render(self.screen)
            
    #handle things
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # handle key events
            #check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w or event.key == pygame.K_UP: # up
                    self.player.up_pressed = True
                    print("up v")
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # down
                    self.player.down_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("down v")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # left
                    self.player.left_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("left v")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # right
                    self.player.right_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("right v")
            #check if key is released and refalsify booleans
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.up_pressed = False
                    print("up ^")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player.down_pressed = False
                    print("down ^")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.left_pressed = False
                    print("left ^")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.right_pressed = False
                    print("right ^")
            