import math
import random

import pygame
import config

vec = pygame.math.Vector2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, main_image_path, x=0, y=0, center=False, scale=False, render_collision_box=False):
        self.path = main_image_path
        pygame.sprite.Sprite.__init__(self)
        self.vel = vec(0, 0)
        
        self.image = pygame.image.load(main_image_path)
        self.images = [self.image]
        self.mask = pygame.mask.from_surface(self.image)

        if scale:
            self.image = pygame.transform.scale(self.image, vec(317, 236))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

        self.hitbox = Hitbox(self.rect.x, self.rect.y, self.rect.w, self.rect.h, main_image_path)
        
        if center:
            self.center()

        self.time_elapsed = 0
        self.animation_counter = 0
        self.animation_frequency = 5

    def render(self, surface, offset, dt):
        self.animate(dt)
        surface.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))

        # Collision box
        #if self.render_collision_box:
        #    pygame.draw.rect(surface, config.RED, pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h), width=1)
        self.hitbox.render(surface, offset, dt)

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


class Map(Sprite):
    def __init__(self, main_image_path, x=0, y=0, center=False, scale=False, render_mask=False):
        super().__init__(main_image_path, x, y, center, scale)
        self.mask.invert()

        self.mask_outline = None
        self.create_outline()

        self.render_mask = render_mask
        # self.rect_list = []
        # self.create_outline_2()

    def change_render_mask(self):
        self.render_mask = not self.render_mask

    def render(self, surface, offset, dt):
        if self.render_mask:
            self.render_outline(surface, offset)

        # for point in self.rect_list:
        #     pygame.draw.rect(surface, config.RED, point)

        # pygame.draw.rect(surface, config.RED, self.mask)

        super().render(surface, offset, dt)

    def create_outline(self):
        self.mask_outline = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask_outline.to_surface()
        self.mask_outline.set_colorkey((0, 0, 0))

    def render_outline(self, surface, offset):
        surface.blit(self.mask_outline, (self.rect.x - offset.x - 1, self.rect.y - offset.y))
        surface.blit(self.mask_outline, (self.rect.x - offset.x + 1, self.rect.y - offset.y))
        surface.blit(self.mask_outline, (self.rect.x - offset.x, self.rect.y - offset.y - 1))
        surface.blit(self.mask_outline, (self.rect.x - offset.x, self.rect.y - offset.y + 1))


class NPC(Sprite):
    def __init__(self, main_image_path, main_fight_sprite_path, music_path="audio/megalovania.ogg", x=0, y=0,
                 center=False, scale=False, hp=50, max_hp=50, boss=False):
        self.music_path = music_path

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

        self.hp = hp
        self.max_hp = max_hp

    def receive_damage(self, dmg):
        if self.hp - dmg > 0:
            self.hp -= dmg
        else:
            self.hp = 0

    def render_hp(self, surface):
        hp_percentage = self.hp / self.max_hp
        pygame.draw.rect(surface, (200, 100, 150), pygame.Rect(99, 9, 102, 12),
                         border_radius=3)
        if self.hp > 0:
            pygame.draw.rect(surface, (255 - 255 * hp_percentage, 255 * hp_percentage, 0),
                             pygame.Rect(100, 10, 100 * hp_percentage, 10),
                             border_radius=3)

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

            # self.fight_image = pygame.transform.rotate(self.fight_image, self.cur_animation_value)

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


class TestNPC(NPC):
    def __init__(self, main_image_path="imgs/older_player.png", main_fight_sprite_path="imgs/older_player.png",
                 music_path="audio/ruins.ogg", x=0, y=0, center=False, scale=False, hp=1, max_hp=1, boss=False):
        super().__init__(main_image_path, main_fight_sprite_path, music_path, x, y, center, scale, hp, max_hp)

        self.images = [pygame.image.load("imgs/older_player.png")]


class Sans(NPC):
    def __init__(self, main_image_path="imgs/sans_1.png", main_fight_sprite_path="imgs/sans_large.png",
                 music_path="audio/megalovania.ogg", x=0, y=0,
                 center=False, scale=False, hp=200, max_hp=200, boss=True):
        super().__init__(main_image_path, main_fight_sprite_path, music_path, x, y, center, scale, hp, max_hp)
        # print(self.rect)
        self.animation_frequency = 1

        self.images = [pygame.image.load("imgs/sans_1.png"), pygame.image.load("imgs/sans_2.png")]

        self.fight_rect.x, self.fight_rect.y = 240, 40


class Bear(NPC):
    def __init__(self, main_image_path="imgs/teddy1.png", main_fight_sprite_path="imgs/fuckedupbear.png",
                 music_path="audio/run.ogg", x=0, y=0,
                 center=False, scale=False, hp=100, max_hp=100, boss=True):
        super().__init__(main_image_path, main_fight_sprite_path, music_path, x, y, center, scale, hp, max_hp)
        # print(self.rect)
        self.animation_frequency = 2

        self.images = [pygame.image.load("imgs/teddy1.png"), pygame.image.load("imgs/teddy2.png")]

        self.fight_rect.x, self.fight_rect.y = 240, 40


class DialogBox(Sprite):
    def __init__(self, main_image_path="imgs/dialog_box.png", x=14, y=136, center=False, scale=False):
        super().__init__(main_image_path, x, y, center, scale)

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


class DialogOption(DialogBox):
    def __init__(self, main_image_path="imgs/dialog_box.png", x=14, y=136, center=False, scale=False):
        super().__init__(main_image_path, x, y, center, scale)

        self.moused_over = False
        self.cur_animation_value = 0
        self.animation_changer = 1
        self.animation_max = 2
        self.animation_frequency = 100

        self.og_pos = vec(x, y)

    def render(self, surface, dt):
        self.animate(dt)
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, dt):
        self.time_elapsed += dt

        if self.time_elapsed > 1000 / self.animation_frequency:
            self.time_elapsed = 0

            self.rect.x, self.rect.y = self.og_pos.x - self.cur_animation_value / 2, self.og_pos.y - self.cur_animation_value / 2

            # self.image = pygame.transform.scale(self.image,
            #                                     vec(self.rect.w + self.cur_animation_value,
            #                                         self.rect.h + self.cur_animation_value))

            if self.moused_over:
                if self.cur_animation_value < self.animation_max:
                    self.cur_animation_value += 1
            else:
                if self.cur_animation_value > 0:
                    self.cur_animation_value -= 1

class Hitbox(pygame.Rect):
    def __init__(self, x, y, width, height, main_image_path):
        self.hitbox = pygame.Rect(x, y, width, height)
            #player hitbox
        self.mask = pygame.mask.from_surface(pygame.image.load(main_image_path))
        self.mask_rect = self.mask.get_rect()
        self.mask_rect.x = x - width / 2
        self.mask_rect.y = y - height / 2


    def render(self, surface, offset, dt):
        hitbox_width_offset = pygame.Rect(self.mask_rect.x - offset.x, self.mask_rect.y - offset.y, self.mask_rect.width, self.mask_rect.height)
        pygame.draw.rect(surface, config.GREEN, hitbox_width_offset, width= 1)
        