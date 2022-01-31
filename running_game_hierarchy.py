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

        self.scene = ""
        self.scenes = dict()

        self.set_up()

    def change_cur_scene(self, new_scene):
        self.scene = new_scene

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
        self.camera.set_method("border")
        self.camera.mode.set_borders(-1000, 1000, -1000, 1000)

        self.cur_indoors_area = ""
        self.indoors_areas = dict()

        self.npc = ""
        self.npcs = dict()

        self.objects = dict()

        self.map: Sprite
        self.set_up()

    def update_indoor_area(self, area_name, area):
        self.indoors_areas[area_name] = area

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.BLUE)

        if self.cur_indoors_area in self.indoors_areas.keys():
            self.indoors_areas.get(self.cur_indoors_area).render(bg_surface)

    def update(self):
        pass


class House(PlayingField):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

        self.room = ""
        self.rooms = dict()

        self.set_up()

    def update_room(self, room_name, room):
        self.rooms[room_name] = room

    def set_up(self):
        pass

    def render(self, bg_surface):
        self.rooms.get(self.room).render(bg_surface)

    def update(self):
        pass


class Room(PlayingField):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)
        self.camera.set_method("stand")

        self.objects = []

        self.npc = ""
        self.npcs = dict()

        self.set_up()

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.BLACK)

        for object in self.objects:
            object.render(bg_surface, self.camera.offset)

    def update(self):
        pass
