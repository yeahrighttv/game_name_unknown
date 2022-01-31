import config
from running_game_hierarchy import Act, MapScene, House, Room


class Entrance(Room):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        pass


class TestHouse(House):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.room = "entrance"
        self.update_room("entrance", Entrance(self.screen, self.game, self.player, self.camera))


class TestScene1(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        pass


class TestScene2(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
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
