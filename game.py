from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []

    def set_up(self):
        player = Player()
        self.objects.append(player)
        print('do se up')

    def update(self):
        print('update')

        for object in self.objects:
            object.render(self.screen)