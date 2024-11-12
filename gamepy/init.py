import pygame
import pygame as pg
import math


pg.init()
time_t = 0.25

#constants
infoObject = pg.display.Info()
width, height = infoObject.current_w, infoObject.current_h
width = 1920
height = 1080
FPS = 60
RADIUS = 10
PLAYER_COLOR = "white"
#video
screen = pg.display.set_mode((width, height), pygame.FULLSCREEN, display=0)
scale_x = width // 1920
scale_y = height // 1080
name = "Game"
clock = pg.time.Clock()
TIME_1 = None
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
