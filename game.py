from functools import partial

import pygame
from pygame.time import Clock
from player import Player
import config
from game_state import GameState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(4.5, 6.4, "imgs/player.png")

        self.player = player
        self.objects.append(player)
        print('do set up')
        self.game_state = GameState.RUNNING

    def render(self):
        for object in self.objects:
            object.render(self.screen)

    # update (loops)
    def update(self):
        self.screen.fill(config.BLACK)
        print('update')
        self.handle_events()
        self.player.update_position()
        self.render()

    # def move(self, right_pressed=False, left_pressed=False, up_pressed=False, down_pressed=False):
    #     if right_pressed:
    #         self.player.right_pressed = True
    #     elif left_pressed:
    #         self.player.left_pressed = True
    #     elif up_pressed:
    #         self.player.up_pressed = True
    #     elif down_pressed:
    #         self.player.down_pressed = True

    # handle things
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED

            # dct = {
            #     pygame.K_w: partial(self.move),
            #     pygame.K_UP: partial(self.move),
            # }

            # handle key events
            # check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED

                elif event.key == pygame.K_w or event.key == pygame.K_UP: # up
                    self.player.direction = "up"
                    self.player.up_pressed = True
                    print("up v")
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # down
                    self.player.direction = "down"
                    self.player.down_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("down v")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # left
                    self.player.direction = "left"
                    self.player.left_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("left v")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # right
                    self.player.direction = "right"
                    self.player.right_pressed = True
                    print(self.player.right_pressed, self.player.left_pressed, self.player.up_pressed, self.player.down_pressed)
                    print("right v")

            # check if key is released and re-falsify booleans
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
