from functools import partial
from os import spawnle
from sprite import Sprite
import pygame
import config


# sprites sorted in lists
walk_up = [pygame.image.load('imgs/player_walk1_up.png'), pygame.image.load('imgs/player_walk2_up.png'), pygame.image.load('imgs/player_walk3_up.png'),  pygame.image.load('imgs/player_walk2_up.png')]
walk_down = [pygame.image.load('imgs/player_walk1_down.png'), pygame.image.load('imgs/player_walk2_down.png'), pygame.image.load('imgs/player_walk3_down.png'),  pygame.image.load('imgs/player_walk2_down.png')]
walk_left = [pygame.image.load('imgs/player_walk1_left.png'), pygame.image.load('imgs/player_walk2_left.png')]
walk_right = [pygame.image.load('imgs/player_walk1_right.png'), pygame.image.load('imgs/player_walk2_right.png')]

directions = {
    "right": walk_right,
    "left": walk_left,
    "up": walk_up,
    "down": walk_down,
}


class Player(Sprite):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        print('Player Created')
        self.velX = 0
        self.velY = 0

        # Store pressed values in player
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.direction = "down"
        self.horizontal_animation_counter = 0
        self.vertical_animation_counter = 0
        self.speed = 0.04

        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE)

    def advance_animation(self):
        self.horizontal_animation_counter += 1
        self.vertical_animation_counter += 1

        if self.vertical_animation_counter >= 4:
            self.vertical_animation_counter = 0
        if self.horizontal_animation_counter >= 2:
            self.horizontal_animation_counter = 0

    def change_vel(self, dirX, dirY):
        self.velX, velY = dirX * self.speed, dirY * self.speed

    def update_position(self):
        # Set velocity back to 0
        self.velX = 0
        self.velY = 0

        # Button press reactions
        if self.direction in ["left", "right"]:
            self.image = directions[self.direction][self.horizontal_animation_counter]
        elif self.direction in ["up", "down"]:
            self.image = directions[self.direction][self.vertical_animation_counter]

        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        if not any([self.right_pressed, self.left_pressed, self.up_pressed, self.down_pressed]):
            self.image = walk_down[1]
        if self.velY == 0 and self.velX == 0:
            self.image = walk_down[1]

        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))

        # Move character according to velocity
        self.x += self.velX
        self.y += self.velY

        # Rescale movement
        self.rect = pygame.Rect(self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE)