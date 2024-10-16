from init import *
import pygame as pg
from button import Button
from scenes.game import Game
from settings import Settings


class Settings(pg.sprite.Sprite):
    def __init__(self):
        self.name = "settings"
        self.game = None
        self.contin = Button("Continue", 0.3, "black")
        self.menu = Button("Menu", 0.6, "black")
        self.qute = Button("Qute", 0.9, "black")

    def __str__(self):
        return self.name