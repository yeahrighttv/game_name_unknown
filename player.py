from os import spawnle
import pygame
import config

#sprites sorted in lists
walk_up = [pygame.image.load('imgs/player_walk1_up.png'), pygame.image.load('imgs/player_walk2_up.png'), pygame.image.load('imgs/player_walk3_up.png'),  pygame.image.load('imgs/player_walk2_up.png')]
walk_down = [pygame.image.load('imgs/player_walk1_down.png'), pygame.image.load('imgs/player_walk2_down.png'), pygame.image.load('imgs/player_walk3_down.png'),  pygame.image.load('imgs/player_walk2_down.png')]
walk_left = [pygame.image.load('imgs/player_walk1_left.png'), pygame.image.load('imgs/player_walk2_left.png')]
walk_right = [pygame.image.load('imgs/player_walk1_right.png'), pygame.image.load('imgs/player_walk2_right.png')]

j = 0
i = 0
#advance index function
def index_advance():
    global j
    global i
    j += 1
    i += 1
    if j >= 4:
        j = 0
    if i >= 2:
        i = 0



stepcount = 0

class Player:
    def __init__(self, x_position, y_position):
        print('Player Created')
        self.x = int(x_position)
        self.y = int(y_position)
        self.velX = 0
        self.velY = 0
        #store pressed values in player
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 0.1
        self.image = pygame.image.load('imgs/player.png')
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print('Player Updated')
    
    def update_position(self):
        global i
        global j
        #set velocity back to 0
        self.velX = 0
        self.velY = 0
        #button press reactions
        if self.left_pressed == True and self.right_pressed == False:
            self.image = walk_left[i]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
            self.velX = -self.speed
        if self.right_pressed == True and self.left_pressed == False:
            self.image = walk_right[i]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
            self.velX = self.speed
        if self.up_pressed == True and self.down_pressed == False:
            self.image = walk_up[j]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
            self.velY = -self.speed
        if self.down_pressed == True and self.up_pressed == False:
            self.image = walk_down[j]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
            self.velY = self.speed
        if self.down_pressed == False and self.up_pressed == False and self.right_pressed == False and self.left_pressed == False:
            self.image = walk_down[1]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        if self.velY == 0 and self.velX == 0:
            self.image = walk_down[1]
            self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        #move character according to velocity
        self.x += self.velX
        self.y += self.velY
        #rescale movement
        self.rect = self.x * config.SCALE, self.y * config.SCALE, config.SCALE, config.SCALE
    def render(self, screen):
        bgsurface = pygame.surface.Surface((316, 236))
        entrance = pygame.image.load('imgs/Room_Entrance.png')
        stairs = pygame.image.load('imgs/Staircase_1.png')
        rail1 = pygame.image.load('imgs/Railing_asset1.png')
        rail2 = pygame.image.load('imgs/Railing_asset2.png')
        rail3 = pygame.image.load('imgs/Railing_asset3.png')

        

        pygame.Surface.blit(bgsurface, stairs, (0,0))
        pygame.Surface.blit(bgsurface, entrance, (0,0))
        bgsurface.blit(self.image, self.rect)
        pygame.Surface.blit(bgsurface, rail1, (0,0))
        pygame.Surface.blit(bgsurface, rail2, (0,0))
        pygame.Surface.blit(bgsurface, rail3, (0,0))

        pygame.transform.scale(bgsurface, (316 * 2, 236 * 2), dest_surface=screen)

        
