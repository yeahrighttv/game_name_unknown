import config
from running_game_hierarchy import Act, MapScene, House, Room, Entrance
from sprite import Sprite, SpriteInsideHouse


class EntranceRoom(Room):
    def set_up(self):
        self.objects["staircase"] = SpriteInsideHouse("imgs/Staircase_1.png", center=True)
        self.objects["bg"] = SpriteInsideHouse("imgs/Room_Entrance.png", center=True)
        self.objects["player"] = self.player
        self.objects["rail_1"] = SpriteInsideHouse("imgs/Railing_asset1.png", center=True)
        self.objects["rail_2"] = SpriteInsideHouse("imgs/Railing_asset2.png", center=True)
        self.objects["rail_3"] = SpriteInsideHouse("imgs/Railing_asset3.png", center=True)

        self.update_entrance("entrance 1", Entrance())
        self.entrances.get("entrance 1").set_default_bottom()

        self.update_entrance("entrance 2", Entrance())
        self.entrances.get("entrance 2").set_default_left_lower()

        self.update_entrance("entrance 3", Entrance())
        self.entrances.get("entrance 3").set_default_right_lower()


class TestHouse(House):
    def set_up(self):
        self.room = "entrance"
        self.update_room("entrance", EntranceRoom(self.screen, self.game, self.player, self.camera, self))
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
