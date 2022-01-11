import pygame
from abc import ABC, abstractmethod
vec = pygame.math.Vector2


class Camera:
    def __init__(self, player, display_vec):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = display_vec.x, display_vec.y
        # self.CONST = vec(-self.DISPLAY_W / 8 + player.rect.w / 8, -self.DISPLAY_W / 8 + player.rect.w / 8)
        self.CONST = vec(-140, -100)
        self.modes = {}

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def set_method(self, mode):
        self.mode = self.modes[mode]

    def scroll(self):
        self.mode.scroll()


class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
        self.east_border_const = 280
        self.south_border_const = 200

        # North, South, West and East borders
        self.borders = {
            "n": -200,
            "s": 200,
            "w": -200,
            "e": 200,
        }

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.borders["w"], self.camera.offset.x)
        self.camera.offset.x = min(self.borders["e"] - self.east_border_const, self.camera.offset.x)
        self.camera.offset.y = max(self.borders["n"], self.camera.offset.y)
        self.camera.offset.y = min(self.borders["s"] - self.south_border_const, self.camera.offset.y)


class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
        self.scroll_speed = 0.1

    def change_scroll_speed(self, new_speed):
        self.scroll_speed = new_speed

    def scroll(self):
        self.camera.offset.x += self.scroll_speed


class Stand(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

    def scroll(self):
        pass
