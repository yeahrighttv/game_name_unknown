import time
from abc import abstractmethod

import pygame

import config
from program_states import AbstractState
from sprite import Sprite

vec = pygame.math.Vector2


class PlayingField(AbstractState):
    def __init__(self, screen, game, player, camera, parent):
        super().__init__(screen, game)
        self.player = player
        self.camera = camera
        self.parent = parent

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
    def update(self, dt):
        self.dt = dt


class Act(PlayingField):
    def __init__(self, screen, game, player, camera, parent):
        super().__init__(screen, game, player, camera, parent)

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

    def update(self, dt):
        self.dt = dt

        self.scenes.get(self.scene).update(dt)


class GeneralScene(PlayingField):
    def __init__(self, screen, game, player, camera, parent):
        super().__init__(screen, game, player, camera, parent)

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def render(self, bg_surface):
        pass

    @abstractmethod
    def update(self, dt):
        self.dt = dt


class MapScene(GeneralScene):
    def __init__(self, screen, game, player, camera, parent):
        super().__init__(screen, game, player, camera, parent)

        self.cur_indoors_area = ""
        self.indoors_areas = dict()

        self.npc = ""
        self.npcs = dict()

        self.objects = dict()

        self.map = None
        self.set_up()

    def update_indoor_area(self, area_name, area):
        self.indoors_areas[area_name] = area

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.BLUE)

        if self.cur_indoors_area in self.indoors_areas.keys():
            self.indoors_areas.get(self.cur_indoors_area).render(bg_surface)
        else:
            self.map.render(bg_surface, self.camera.offset, self.dt)

            for object in self.objects.values():
                object.render(bg_surface, self.camera.offset, self.dt)

            for npc in self.npcs.values():
                npc.render(bg_surface, self.camera.offset, self.dt)

            for area in self.indoors_areas.values():
                area.render_house(bg_surface)

            self.player.render(bg_surface, self.camera.offset, self.dt)

    def update(self, dt):
        self.dt = dt

        self.camera.set_method("border")
        self.camera.mode.set_borders(-4000, 4000, -4000, 4000)

        if self.cur_indoors_area in self.indoors_areas.keys():
            self.indoors_areas.get(self.cur_indoors_area).update(dt)
        else:
            self.player.scope = self.map
            for area_name, area in self.indoors_areas.items():
                if self.player.rect.colliderect(area.house_sprite.rect):
                    self.cur_indoors_area = area_name
                    self.indoors_areas.get(self.cur_indoors_area).enter_house()
                    time.sleep(0.5)
                    break


class House(PlayingField):
    def __init__(self, screen, game, player, camera, parent):
        super().__init__(screen, game, player, camera, parent)

        self.house_sprite = None

        self.room = ""
        self.entry_room = ""
        self.rooms = dict()

        self.set_up()

    def set_entry_name(self, entry_room_name):
        self.entry_room = entry_room_name

    def enter_house(self):
        self.room = self.entry_room
        self.rooms.get(self.room).enter_room()

    def set_room_by_name(self, room_name):
        self.room = room_name

    def update_room(self, room_name, room):
        self.rooms[room_name] = room

    def set_up(self):
        pass

    def render(self, bg_surface):
        self.rooms.get(self.room).render(bg_surface)

    def render_house(self, bg_surface):
        self.house_sprite.render(bg_surface, self.camera.offset, self.dt)

    def update(self, dt):
        self.dt = dt

        self.rooms.get(self.room).update(dt)


class Room(PlayingField):
    def __init__(self, room_name, screen, game, player, camera, parent):
        super().__init__(screen, game, player, camera, parent)

        self.room_name = room_name

        self.entrances = dict()

        self.objects = dict()

        self.npc = ""
        self.npcs = dict()

        self.default_entrance = ""

        self.set_up()

    def enter_room(self, entrance=None):
        self.player.scope = self.objects.get("bg")
        if entrance is None:
            self.player.rect.x, self.player.rect.y = self.entrances.get(self.default_entrance).get_player_pos()
        else:
            self.player.rect.x, self.player.rect.y = self.entrances.get(entrance).get_player_pos()

    def return_outside(self, return_side_of_house="w"):
        self.parent.parent.cur_indoors_area = ""

        house_sides_coords = {
            "w": (self.parent.house_sprite.rect.x - self.player.rect.w, self.parent.house_sprite.rect.y),
            "e": (self.parent.house_sprite.rect.x + self.player.rect.w, self.parent.house_sprite.rect.y),
            "n": (self.parent.house_sprite.rect.x, self.parent.house_sprite.rect.y - self.player.rect.h),
            "s": (self.parent.house_sprite.rect.x, self.parent.house_sprite.rect.y + self.player.rect.h),
        }
        self.player.rect.x, self.player.rect.y = house_sides_coords.get(return_side_of_house,
                                                                        (self.parent.house_sprite.rect.x - self.player.rect.w, self.parent.house_sprite.rect.y))

        self.player.scope = self.parent.parent.map

    def update_entrance(self, entrance_name, entrance):
        self.entrances[entrance_name] = entrance

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.BLACK)

        for object in self.objects.values():
            object.render(bg_surface, self.camera.offset, self.dt)

        for npc in self.npcs.values():
            npc.render(bg_surface, self.camera.offset, self.dt)

        for entrance in self.entrances.values():
            entrance.render(bg_surface, self.camera.offset, self.dt)

    def update(self, dt):
        self.dt = dt

        self.camera.set_method("stand")
        self.camera.offset = vec(self.camera.CONST.x, self.camera.CONST.y)

        for entrance in self.entrances.values():
            if self.player.rect.colliderect(entrance.rect):
                entrance.action()
                self.parent.set_room_by_name(entrance.destination_name)
                if self.parent.room in self.parent.rooms:
                    self.parent.rooms.get(self.parent.room).enter_room(self.room_name)


class Entrance:
    def __init__(self, player, destination_name, enter_from, x=0, y=0, width=16, height=16):
        self.player = player
        self.rect = pygame.Rect(x, y, width, height)
        self.destination_name = destination_name
        self.enter_from = enter_from

    def get_player_pos(self):
        player_pos_from_entering = {
            "w": (self.rect.x + self.rect.w, self.rect.y),
            "e": (self.rect.x - self.player.rect.w, self.rect.y),
            "n": (self.rect.x, self.rect.y + self.rect.h),
            "s": (self.rect.x, self.rect.y - self.player.rect.h),
        }

        return player_pos_from_entering.get(self.enter_from)

    def action(self):
        time.sleep(0.5)

    def set_default_south(self):
        self.set_pos(-16, 116)
        self.set_shape(32, 2)

    def set_default_north(self):
        self.set_pos(-16, -118)
        self.set_shape(32, 2)

    def set_default_west(self):
        self.set_pos(-158, -16)
        self.set_shape(2, 32)

    def set_default_west_lower(self):
        self.set_pos(-158, 44)
        self.set_shape(2, 32)

    def set_default_west_center_lower(self):
        self.set_pos(-158, 10)
        self.set_shape(2, 32)

    def set_default_east(self):
        self.set_pos(157, -16)
        self.set_shape(2, 32)

    def set_default_east_lower(self):
        self.set_pos(157, 44)
        self.set_shape(2, 32)

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y

    def set_shape(self, w, h):
        self.rect.w, self.rect.h = w, h

    def render(self, surface, offset):
        pygame.draw.rect(surface, config.BLUE,
                         pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h), width=1)


class HorizontalEntrance(Entrance):
    def __init__(self, player, destination_name, enter_from, x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_shape(32, 2)


class NorthEntrance(HorizontalEntrance):
    def __init__(self, player, destination_name, enter_from="n", x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_default_north()


class SouthEntrance(HorizontalEntrance):
    def __init__(self, player, destination_name, enter_from="s", x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_default_south()


class VerticalEntrance(Entrance):
    def __init__(self, player, destination_name, enter_from, x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_shape(2, 32)


class WestEntrance(HorizontalEntrance):
    def __init__(self, player, destination_name, enter_from="w", x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_default_west()


class EastEntrance(HorizontalEntrance):
    def __init__(self, player, destination_name, enter_from="e", x=0, y=0, width=16, height=16):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.set_default_east()


class ReturnEntrance(Entrance):
    def __init__(self, room, player, destination_name="", enter_from="", x=0, y=0, width=16, height=16,
                 return_side="w"):
        super().__init__(player, destination_name, enter_from, x, y, width, height)
        self.room = room
        self.return_side = return_side

    def action(self):
        self.room.return_outside(self.return_side)
        time.sleep(0.5)
