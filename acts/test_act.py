import config
from running_game_hierarchy import Act, MapScene, House, Room, Entrance, ReturnEntrance
from sprite import Sprite, SpriteInsideHouse


class RoomEastHallway(Room):
    def set_up(self):
        self.enter_from_default = "w"
        self.add_entry_pos("w", -156, 10)

        self.objects["bg"] = SpriteInsideHouse("imgs/Assets/EastHallway.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance 1", Entrance("entrance", "e"))
        self.entrances.get("entrance 1").set_default_left_center_lower()


class RoomWest(Room):
    def set_up(self):
        self.enter_from_default = "e"
        self.add_entry_pos("e", 125, 44)

        self.objects["bg_walls"] = SpriteInsideHouse("imgs/Assets/Room_West_Walls.png", center=True)
        self.objects["bg_floor"] = SpriteInsideHouse("imgs/Assets/Room_West_Floor.png", center=True)
        self.objects["player"] = self.player

        self.update_entrance("entrance 1", Entrance("entrance", "w"))
        self.entrances.get("entrance 1").set_default_right_lower()


class EntranceRoom(Room):
    def set_up(self):
        self.enter_from_default = "s"
        self.add_entry_pos("s", -16, 84)
        self.add_entry_pos("w",  -156, 44)
        self.add_entry_pos("e",  125, 44)

        self.objects["staircase"] = SpriteInsideHouse("imgs/Staircase_1.png", center=True)
        self.objects["bg"] = SpriteInsideHouse("imgs/Room_Entrance.png", center=True)
        self.objects["player"] = self.player
        self.objects["rail_1"] = SpriteInsideHouse("imgs/Railing_asset1.png", center=True)
        self.objects["rail_2"] = SpriteInsideHouse("imgs/Railing_asset2.png", center=True)
        self.objects["rail_3"] = SpriteInsideHouse("imgs/Railing_asset3.png", center=True)

        self.update_entrance("entrance 1", ReturnEntrance(self, "", return_side="w"))
        self.entrances.get("entrance 1").set_default_bottom()

        self.update_entrance("entrance 2", Entrance("west_room", "e"))
        self.entrances.get("entrance 2").set_default_left_lower()

        self.update_entrance("entrance 3", Entrance("east_hallway", "w"))
        self.entrances.get("entrance 3").set_default_right_lower()


class TestHouse(House):
    def set_up(self):
        self.set_entry_name("entrance")
        self.update_room("entrance", EntranceRoom(self.screen, self.game, self.player, self.camera, self))
        self.update_room("west_room", RoomWest(self.screen, self.game, self.player, self.camera, self))
        self.update_room("east_hallway", RoomEastHallway(self.screen, self.game, self.player, self.camera, self))
        self.house_sprite = Sprite("imgs/house_test.png", 100, 100, center=True)


class TestScene1(MapScene):
    def set_up(self):
        self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))


class TestScene2(MapScene):
    def set_up(self):
        self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.cur_indoors_area = "house 1"
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera, self))

    # def render(self, bg_surface):
    #     bg_surface.fill(config.GREEN)


class TestAct(Act):
    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene1(self.screen, self.game, self.player, self.camera, self))
        self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera, self))
