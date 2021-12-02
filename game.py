import pygame
from player import Player, pressedkeys, stepcount
import config
from game_state import GameState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print('do set up')
        self.game_state = GameState.RUNNING

#        self.

    def update(self):
        self.screen.fill(config.BLACK)
        print('update')
        self.handle_events()

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # hanlde key events
            #check if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w or event.key == pygame.K_UP: # up
                    #self.player.update_position(0, -1)
                    pressedkeys['up'] = True
                    print("up v")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # down
                    #self.player.update_position(0, 1)
                    pressedkeys['down'] = True
                    print("down v")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # left
                    #self.player.update_position(-1, 0)
                    pressedkeys['left'] = True
                    print("left v")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # right
                    #self.player.update_position(1, 0)
                    pressedkeys['right'] = True
                    print("right v")
            #check if key is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pressedkeys['up'] = False
                    print("up ^")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pressedkeys['down'] = False
                    print("down ^")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pressedkeys['left'] = False
                    print("left ^")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pressedkeys['right'] = False
                    print("right ^")
            #if key is pressed: change posistion
            if pressedkeys['up']:
                pygame.time.wait(50)
                self.player.update_position(0, -1)
            if pressedkeys['down']:
                pygame.time.wait(50)
                self.player.update_position(0, 1)
            if pressedkeys['left']:
                pygame.time.wait(50)
                self.player.update_position(-1, 0)
            if pressedkeys['right']:
                pygame.time.wait(50)
                self.player.update_position(1, 0)
#check if keys are pressed
