from functools import partial
from os import spawnle
from sprite import Sprite, Item
import pygame
import config

vec = pygame.math.Vector2


class Player(Sprite):
    def __init__(self, main_image_path, x, y, center=False, scale=False):
        super().__init__(main_image_path, x, y, center, scale)

        self.inventory = Inventory()

        self.name = "Anon"
        self.dmg = 51
        self.hp = 17
        self.max_hp = 20
        self.xp = 5
        self.max_xp = 20
        self.lvl = 0

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
        self.mask = pygame.mask.from_surface(pygame.image.load('imgs/player_walk1_down.png'))
        self.mask_rect = self.mask.get_rect()

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


class Inventory:
    def __init__(self, max_len=16):
        self.items = dict()
        self.max_len = max_len
        self.id = 0

    def create_item(self, main_image_path, display_name="Unknown",
                 desc="Item without a description", x=0, y=0, center=False, scale=False,
                 render_collision_box=False, margin=vec(30, 15), step=30):
        self.id += 1
        dict_name = f"{display_name} {self.id}"
        item = Item(main_image_path, display_name, dict_name, self.id, desc,
                    x, y, center, scale, render_collision_box,
                    margin, step)

        return item

    def check_if_can_add(self):
        return len(self.items) + 1 <= self.max_len

    def add_item(self, item):
        if self.check_if_can_add():
            self.items[item.dict_name] = item

    def remove_item(self, item_name):
        self.items.pop(item_name)

    def render_inventory(self, surface, start_at):
        for i, item in enumerate(self.items.values()):
            item.render_item_in_box(surface, start_at, i)
