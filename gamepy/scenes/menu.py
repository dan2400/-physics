from init import *
import pygame as pg
from button import Button
from game import Game
from settings import Settings


class Menu(pg.sprite.Sprite):
    def __init__(self):
        self.name = "menu"
        self.game = None
        self.start = Button("Start", 0.3, "black")

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["red"])
        self.start.draw_but(screen)

    def new_game(self):
        self.game = Game()

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            menu.start.prepare(screen)

    def mouse_button_up(self, event):
        global status
        if event.type == pg.MOUSEBUTTONUP:
            if menu.start.push():
                menu.new_game()
                status = "game"

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                status = "settings"