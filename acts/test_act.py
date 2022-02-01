import config
from running_game_hierarchy import Act, MapScene, House, Room
from sprite import Sprite, SpriteInsideHouse


class Entrance(Room):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.objects["staircase"] = SpriteInsideHouse("imgs/Staircase_1.png", center=True)
        self.objects["bg"] = SpriteInsideHouse("imgs/Room_Entrance.png", center=True)
        self.objects["player"] = self.player
        self.objects["rail_1"] = SpriteInsideHouse("imgs/Railing_asset1.png", center=True)
        self.objects["rail_2"] = SpriteInsideHouse("imgs/Railing_asset2.png", center=True)
        self.objects["rail_3"] = SpriteInsideHouse("imgs/Railing_asset3.png", center=True)


class TestHouse(House):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.room = "entrance"
        self.update_room("entrance", Entrance(self.screen, self.game, self.player, self.camera))
        self.house_sprite = Sprite("imgs/house_test.png", 100, 100, center=True)


class TestScene1(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera))


class TestScene2(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.map = Sprite("imgs/zelda_map_test.png", center=True)
        self.cur_indoors_area = "house 1"
        self.update_indoor_area("house 1", TestHouse(self.screen, self.game, self.player, self.camera))

    # def render(self, bg_surface):
    #     bg_surface.fill(config.GREEN)


class TestAct(Act):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene1(self.screen, self.game, self.player, self.camera))
        self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera))
