import config
from running_game_hierarchy import Act, MapScene


class TestScene1(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        pass


class TestScene2(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        pass

    def render(self, bg_surface):
        bg_surface.fill(config.GREEN)


class TestAct(Act):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene1(self.screen, self.game, self.player, self.camera))
        self.update_scene("scene 2", TestScene2(self.screen, self.game, self.player, self.camera))
