import config
from running_game_hierarchy import Act, MapScene


class TestScene(MapScene):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        pass


class TestAct(Act):
    def __init__(self, screen, game, player, camera):
        super().__init__(screen, game, player, camera)

    def set_up(self):
        self.scene = "scene 1"
        self.update_scene("scene 1", TestScene(self.screen, self.game, self.player, self.camera))
