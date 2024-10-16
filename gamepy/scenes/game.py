from init import *
import pygame as pg
from button import Button
from game import Game
from settings import Settings


class Game(pg.sprite.Sprite):
    def __init__(self):
        self.name = "game"

    def __str__(self):
        return self.name
    def draw(self):
        screen.fill(colors["black"])
        all_sprites.update()
        all_sprites.draw(screen)

    def key_down(self, event):
        global status
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                status = "settings"