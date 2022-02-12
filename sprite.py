import math
import random

import pygame
import config

vec = pygame.math.Vector2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, main_image_path, x=0, y=0, center=False, scale=False):
        self.path = main_image_path
        pygame.sprite.Sprite.__init__(self)

        self.vel = vec(0, 0)

        self.image = pygame.image.load(main_image_path)
        self.images = [self.image]
        if scale:
            self.image = pygame.transform.scale(self.image, vec(317, 236))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

        if center:
            self.center()

        self.time_elapsed = 0
        self.animation_counter = 0
        self.animation_frequency = 5

    def render(self, surface, offset, dt):
        self.animate(dt)
        surface.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

        # Collision box
        pygame.draw.rect(surface, config.RED, pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h), width=1)

    def center(self):
        self.rect.update(self.rect.x + (-self.rect.w / 2),
                         self.rect.y + (-self.rect.h / 2),
                         self.rect.w,
                         self.rect.h)

    def animate(self, dt):
        self.time_elapsed += dt

        if self.time_elapsed > 1000 / self.animation_frequency:
            self.time_elapsed = 0
            self.image = self.images[self.animation_counter]
            self.animation_counter += 1
            if self.animation_counter >= len(self.images):
                self.animation_counter = 0


class NPC(Sprite):
    def __init__(self, main_image_path, main_fight_sprite_path, x=0, y=0, center=False, scale=False):
        super().__init__(main_image_path, x, y, center, scale)
        self.dialogs = dict()

        self.fight_animation_frequency = 10
        self.fight_image = pygame.image.load(main_fight_sprite_path)
        self.fight_images = [self.fight_image]
        self.fight_rect = self.fight_image.get_rect()
        self.animation_fight_counter = 0

        self.cur_animation_value = 0
        self.animation_changer = 1
        self.animation_min, self.animation_max = -4, 4

        self.fight_rect.x, self.fight_rect.y = 240, 40

    def render_fight(self, surface, dt):
        self.animate_fight(dt)
        surface.blit(self.fight_image, (self.fight_rect.x, self.fight_rect.y))

    def animate_fight(self, dt):
        self.time_elapsed += dt

        if self.time_elapsed > 1000 / self.fight_animation_frequency:
            self.time_elapsed = 0
            self.fight_image = self.fight_images[self.animation_fight_counter]
            self.animation_fight_counter += 1
            if self.animation_fight_counter >= len(self.fight_images):
                self.animation_fight_counter = 0

            self.fight_image = pygame.transform.scale(self.fight_image,
                                                      vec(self.fight_rect.w + self.cur_animation_value,
                                                          self.fight_rect.h + self.cur_animation_value))

            self.fight_rect.x, self.fight_rect.y = 240 - self.cur_animation_value / 2, 40 - self.cur_animation_value / 2

            self.cur_animation_value += self.animation_changer
            if self.cur_animation_value >= self.animation_max:
                self.animation_changer = -1
            elif self.cur_animation_value <= self.animation_min:
                self.animation_changer = 1

    def add_empty_dialog(self, name):
        self.dialogs[name] = []

    def add_dialog_string_to_name(self, name, new_string):
        self.dialogs[name].append(new_string)


class Sans(NPC):
    def __init__(self, main_image_path="imgs/sans_1.png", main_fight_sprite_path="imgs/sans_large.png", x=0, y=0,
                 center=False, scale=False):
        super().__init__(main_image_path, main_fight_sprite_path, x, y, center, scale)
        # print(self.rect)
        self.animation_frequency = 1

        self.images = [pygame.image.load("imgs/sans_1.png"), pygame.image.load("imgs/sans_2.png")]

        self.fight_rect.x, self.fight_rect.y = 240, 40


class DialogBox(pygame.sprite.Sprite):
    def __init__(self, main_image_path="imgs/dialog_box.png", x=14, y=140, center=False, scale=False):
        self.path = main_image_path
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(main_image_path)
        self.images = [self.image]
        if scale:
            self.image = pygame.transform.scale(self.image, vec(317, 236))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

        if center:
            self.center()

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def center(self):
        self.rect.update(self.rect.x + (-self.rect.w / 2),
                         self.rect.y + (-self.rect.h / 2),
                         self.rect.w,
                         self.rect.h)
