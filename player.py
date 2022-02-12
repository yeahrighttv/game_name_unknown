from functools import partial
from os import spawnle
from sprite import Sprite
import pygame
import config

vec = pygame.math.Vector2


class Player(Sprite):
    def __init__(self, path, x, y, center=False):
        super().__init__(path, x, y)
        self.scope = None

        # print('Player Created')
        self.vel = vec(0, 0)

        self.horizontal_animation_counter = 0
        self.vertical_animation_counter = 0
        self.speed = 1

        if center:
            self.center()

        walk_up = [pygame.image.load('imgs/player_walk1_up.png'), pygame.image.load('imgs/player_walk2_up.png'),
                   pygame.image.load('imgs/player_walk3_up.png'), pygame.image.load('imgs/player_walk2_up.png')]
        walk_down = [pygame.image.load('imgs/player_walk1_down.png'), pygame.image.load('imgs/player_walk2_down.png'),
                     pygame.image.load('imgs/player_walk3_down.png'), pygame.image.load('imgs/player_walk2_down.png')]
        walk_left = [pygame.image.load('imgs/player_walk1_left.png'), pygame.image.load('imgs/player_walk2_left.png')]
        walk_right = [pygame.image.load('imgs/player_walk1_right.png'),
                      pygame.image.load('imgs/player_walk2_right.png')]

        self.directions = {
            "right": walk_right,
            "left": walk_left,
            "up": walk_up,
            "down": walk_down,
        }

    def advance_animation(self):
        self.horizontal_animation_counter += 1
        self.vertical_animation_counter += 1

        if self.vertical_animation_counter >= 4:
            self.vertical_animation_counter = 0
        if self.horizontal_animation_counter >= 2:
            self.horizontal_animation_counter = 0

    def change_direction(self):

        # Temp fix for directions by ordering updates
        if self.vel.y < 0:
            self.image = self.directions["up"][self.vertical_animation_counter]
        elif self.vel.y > 0:
            self.image = self.directions["down"][self.vertical_animation_counter]
        elif self.vel.x > 0:
            self.image = self.directions["right"][self.horizontal_animation_counter]
        elif self.vel.x < 0:
            self.image = self.directions["left"][self.horizontal_animation_counter]
        else:
            self.image = self.directions["down"][1]

    def change_vel(self, dirX, dirY):
        self.vel.xy = dirX * self.speed, dirY * self.speed

    def move(self, dirX, dirY):
        self.update_position(dirX, dirY)
        self.change_direction()

    def update_position(self, dirX, dirY):
        self.change_vel(dirX, dirY)

        # Move rect
        if self.scope is None:
            self.rect.move_ip(self.vel)
        else:
            if self.scope.rect.contains(pygame.Rect(self.rect.x + self.vel.x,
                                               self.rect.y + self.vel.y,
                                               self.rect.w,
                                               self.rect.h)):
                self.rect.move_ip(self.vel)

    def center(self):
        self.rect.update(self.rect.x + (-self.rect.w / 2),
                         self.rect.y + (-self.rect.h / 2),
                         self.rect.w,
                         self.rect.h)
        # print(self.rect)


