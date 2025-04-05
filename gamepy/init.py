import pygame
import pygame as pg
import math
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False


pg.init()
time_t = 0.25

#constants
infoObject = pg.display.Info()
width_x, height_y = infoObject.current_w, infoObject.current_h
width = width_x
height = height_y

#temp
width_x = 1920
height_y = 1080

width = 640
height = 360
FPS = 60
RADIUS = 10
PLAYER_COLOR = "white"
print(width, height)
#video
screen = pg.display.set_mode((width_x, height_y), pygame.FULLSCREEN, display=0)
scale_x = width_x // 640
scale_y = height_y // 360
name = "Game"
clock = pg.time.Clock()
TIME_1 = None
#simulation
draw_o = pymunk.pygame_util.DrawOptions(screen)
space = pymunk.Space()
space.gravity = 0, 8000
#game consts
enemies = pg.sprite.Group()
all_sprites = pg.sprite.Group()
horisontal = pg.sprite.Group()
vertical = pg.sprite.Group()
sound = pg.sprite.Group()
lever_sprite = pg.sprite.Group()
#colors
colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0)
}
