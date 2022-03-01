from functools import partial
from os import spawnle
from sprite import Sprite
import pygame
import config

vec = pygame.math.Vector2


class Player(Sprite):
    def __init__(self, main_image_path, x, y, center=False, scale=False):
        super().__init__(main_image_path, x, y, center, scale)

        self.dmg = 51

        # print('Player Created')
        self.vel = vec(0, 0)

        self.horizontal_animation_counter = 0
        self.vertical_animation_counter = 0
        # pixels / s
        self.speed = 200

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

    def change_speed(self, new_speed):
        self.speed = new_speed

    def animate(self, dt):
        self.time_elapsed += dt

        # print(self.time_elapsed, dt)

        if self.time_elapsed > 1000 / self.animation_frequency:
            self.time_elapsed = 0

            self.horizontal_animation_counter += 1
            self.vertical_animation_counter += 1
            if self.vertical_animation_counter >= len(self.directions["up"]):
                self.vertical_animation_counter = 0
            if self.horizontal_animation_counter >= len(self.directions["left"]):
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

    def move(self, dirX, dirY, dt):
        self.update_position(dirX, dirY, dt)
        self.change_direction()

    def update_position(self, dirX, dirY, dt):
        self.change_vel(dirX * (dt / 1000), dirY * (dt / 1000))

        # Move rect
        self.rect.move_ip(self.vel)

    def center(self):
        self.rect.update(self.rect.x + (-self.rect.w / 2), self.rect.y + (-self.rect.h / 2), self.rect.w, self.rect.h)


