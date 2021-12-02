import pygame
import config

#sprites sorted in lists
walk_up = [pygame.image.load('imgs/player_walk1_up.png'), pygame.image.load('imgs/player_walk2_up.png'), pygame.image.load('imgs/player_walk3_up.png'), ]
walk_down = [pygame.image.load('imgs/player_walk1_down.png'), pygame.image.load('imgs/player_walk2_down.png'), pygame.image.load('imgs/player_walk3_down.png'), ]
walk_left = [pygame.image.load('imgs/player_walk1_left.png'), pygame.image.load('imgs/player_walk2_left.png')]
walk_right = [pygame.image.load('imgs/player_walk1_right.png'), pygame.image.load('imgs/player_walk2_right.png')]

#check if keys are pressed
pressedkeys = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

stepcount = 0

class Player:
    def __init__(self, x_position, y_position):
        print('Player Created')
        self.position = [x_position, y_position]
        if pressedkeys['down']:
            self.image = walk_down[1]
        elif pressedkeys['up']:
            self.image = walk_up[1]
        elif pressedkeys['left']:
            self.image = walk_left[1]
        elif pressedkeys['right']:
            self.image = walk_right[1]
        else:
            self.image = pygame.image.load('imgs/player.png')
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print('Player Updated')
    
    def update_position(self, x_change, y_change):
        global stepcount
        self.position[0] += x_change
        self.position[1] += y_change
        self.rect = self.position[0] * config.SCALE/10, self.position[1] * config.SCALE/10, config.SCALE, config.SCALE
    def render(self, screen):
        screen.blit(self.image, self.rect)