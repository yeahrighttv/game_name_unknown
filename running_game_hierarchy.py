from abc import abstractmethod

import pygame

import config
from program_states import AbstractState
from sprite import Sprite


class PlayingField(AbstractState):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game)
        self.player = player
        self.camera = camera

        self.flags = dict()

    def update_flags(self, flag_name, flag: bool):
        """Can be used to add and update flags"""
        self.flags[flag_name] = flag

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def render(self, bg_surface):
        pass

    @abstractmethod
    def update(self):
        pass


class Act(PlayingField):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

        self.scene = "scene 1"
        self.scenes = dict()

        self.set_up()

    def update_scene(self, scene_name, scene):
        """Can be used to add and update scenes"""
        self.scenes[scene_name] = scene

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.RED)
        self.scenes.get(self.scene).render(bg_surface)

    def update(self):
        self.scenes.get(self.scene).update()


class GeneralScene(PlayingField):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def render(self, bg_surface):
        pass

    @abstractmethod
    def update(self):
        pass


class MapScene(GeneralScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

        self.cur_indoors_area = None
        self.indoors_areas = dict()

        self.npc = None
        self.npcs = dict()

        self.map = Sprite("imgs/zelda_map_test.png")
        self.set_up()

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.BLUE)

    def update(self):
        pass