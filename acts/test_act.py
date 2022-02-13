import config
from running_game_hierarchy import Act, MapScene, House, Room, Entrance, ReturnEntrance, EastEntrance, NorthEntrance, \
    SouthEntrance, WestEntrance
from sprite import Sprite, Sans, Map


class Kitchen(Room):
    def set_up(self):
        self.default_entrance = "west_room"

        self.objects["bg"] = Sprite("imgs/Kitchen.png", -33, 36, center=True, scale=False)
        self.objects["player"] = self.player

        self.update_entrance("west_room", SouthEntrance(self.player, "west_room"))
        self.entrances.get("west_room").set_shape(32, 2)
        self.entrances.get("west_room").set_pos(-80, 116)

        self.update_entrance("secret_1", NorthEntrance(self.player, "west_room"))
        self.update_entrance("secret_2", WestEntrance(self.player, "west_room"))
        self.update_entrance("secret_3", EastEntrance(self.player, "west_room"))


class EastHallway(Room):
    def set_up(self):
        self.default_entrance = "entrance room"

        self.objects["bg"] = Sprite("imgs/Assets/EastHallway.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance_room", WestEntrance(self.player, "entrance_room"))
        self.entrances.get("entrance_room").set_default_west_center_lower()

        self.update_entrance("secret_1", SouthEntrance(self.player, "entrance_room"))

        self.npcs["sans"] = Sans(x=100, y=0, center=True)


class WestRoom(Room):
    def set_up(self):
        self.default_entrance = "entrance room"
        self.objects["bg"] = Sprite("imgs/Assets/Room_West_Walls.png", center=True)
        self.objects["bg_floor"] = Sprite("imgs/Assets/Room_West_Floor.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance_room", EastEntrance(self.player, "entrance_room"))
        self.entrances.get("entrance_room").set_default_east_lower()

        self.update_entrance("kitchen", NorthEntrance(self.player, "kitchen"))
        self.entrances.get("kitchen").set_shape(32, 2)
        self.entrances.get("kitchen").set_pos(-110, -118)


class EntranceRoom(Room):
    def set_up(self):

        self.default_entrance = "entrance_room"

        self.objects["staircase"] = Sprite("imgs/Staircase_1.png", center=True)
        self.objects["bg"] = Sprite("imgs/Room_Entrance.png", center=True)
        self.objects["player"] = self.player
        self.objects["rail_1"] = Sprite("imgs/Railing_asset1.png", center=True)
        self.objects["rail_2"] = Sprite("imgs/Railing_asset2.png", center=True)
        self.objects["rail_3"] = Sprite("imgs/Railing_asset3.png", center=True)

        self.update_entrance("entrance_room", ReturnEntrance(self, self.player, enter_from="s", return_side="w"))
        self.entrances.get("entrance_room").set_default_south()

        self.update_entrance("west_room", WestEntrance(self.player, "west_room"))
        self.entrances.get("west_room").set_default_west_lower()

        self.update_entrance("east_hallway", EastEntrance(self.player, "east_hallway"))
        self.entrances.get("east_hallway").set_default_east_lower()


class TestHouse(House):
    def set_up(self):
        self.set_entry_name("entrance_room")
        self.update_room("entrance_room", EntranceRoom("entrance_room", self.screen, self.game, self.player, self.camera, self))
        self.update_room("west_room", WestRoom("west_room", self.screen, self.game, self.player, self.camera, self))
        self.update_room("east_hallway", EastHallway("east_hallway", self.screen, self.game, self.player, self.camera, self))
        self.update_room("kitchen", Kitchen("kitchen", self.screen, self.game, self.player, self.camera, self))
        self.house_sprite = Sprite("imgs/house_test.png", 100, 100, center=True)


class TestScene1(MapScene):
    def set_up(self):
        self.map = Map("imgs/ruins.png", center=True)
        # self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
        self.player.rect.x, self.player.rect.y = -4620, 1450


# class TestScene2(MapScene):
#     def set_up(self):
#         self.map = Sprite("imgs/zelda_map_test.png", center=True)
#         self.cur_indoors_area = "house 1"
#         self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))
#         self.indoors_areas.get(self.cur_indoors_area).enter_house()


class TestAct(Act):
    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene1(self.screen, self.game, self.player, self.camera, self))
        # self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera, self))
