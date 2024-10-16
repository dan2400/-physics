from init import *
from settings import *
from sprites import *
from tilemap import *
from camera import *
from player import *
from sound import *
from button import *
from numba import njit
import dotenv
import os

dotenv.load_dotenv()


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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["STATUS"] = "settings"


class Menu(pg.sprite.Sprite):
    def __init__(self):
        self.name = "menu"
        self.game = None
        self.start = Button("Start", 0.3, "black", self.name)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["red"])
        self.start.draw_but(screen)

    # def new_game(self):
    #     global all_scenes
    #     all_scenes["game"] = Game()
    #     # self.game = Lever()

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start.push():
                self.start.prepare(screen)

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if self.start.push():
                # self.new_game()
                os.environ["STATUS"] = "choice"

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["STATUS"] = "settings"

class Settings(pg.sprite.Sprite):
    def __init__(self):
        self.name = "settings"
        self.game = None
        self.contin = Button("Continue", 0.3, "black", self.name)
        self.menu = Button("Menu", 0.6, "black", self.name)
        self.qute = Button("Qute", 0.9, "black", self.name)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["green"])
        self.contin.draw_but(screen)
        self.menu.draw_but(screen)
        self.qute.draw_but(screen)

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start.push():
                self.start.prepare(screen)

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if self.start.push():
                # self.new_game()
                os.environ["STATUS"] = "choice"

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                global run
                run = False


class Lever(pg.sprite.Sprite):
    def __init__(self):
        self.name = "lever"
        self.game = None

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["black"])
        lever_sprite.update()
        lever_sprite.draw(screen)

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:

            Leaver_sprite_mass()

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["STATUS"] = "settings"

class Choice(pg.sprite.Sprite):
    def __init__(self):
        self.name = "choice"
        self.game = None
        self.buttons = {
            "lever": Button("Lever", 0.3, "black", self.name),
        }

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["blue"])
        for _, button in self.buttons.items():
            button.draw_but(screen)

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for _, button in self.buttons.items():
                if button.push():
                    button.prepare(screen)
                    break

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            for _, button in self.buttons.items():
                if button.push():
                    os.environ["STATUS"] = "lever"
                    break

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["STATUS"] = "menu"


# player = Player()
if __name__ == '__main__':
    run = True
    all_scenes = {
        "menu": Menu(),
        "game": Game(),
        "settings": Settings(),
        "lever": Lever(),
        "choice": Choice(),
    }

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False


            if os.environ.get("STATUS", default="main") == "game":
                all_scenes["game"].draw()
                all_scenes["game"].key_down(event)

            if os.environ.get("STATUS", default="main") == "settings":
                all_scenes["settings"].draw()

            if os.environ.get("STATUS", default="main") == "choice":
                all_scenes["choice"].draw()
                all_scenes["choice"].mouse_button_down(event)
                all_scenes["choice"].mouse_button_up(event)
                all_scenes["choice"].key_down(event)

            if os.environ.get("STATUS", default="main") == "lever":
                all_scenes["lever"].key_down(event)
                all_scenes["lever"].mouse_button_up(event)

            if os.environ.get("STATUS", default="main") == "menu":
                all_scenes["menu"].draw()
                all_scenes["menu"].mouse_button_down(event)
                all_scenes["menu"].mouse_button_up(event)
                all_scenes["menu"].key_down(event)

        if os.environ.get("STATUS", default="main") == "lever":
            all_scenes["lever"].draw()


        if show_fps:
            fps = str(int(clock.get_fps()))
            font = pg.font.Font(None, 20)
            screen.blit(font.render(fps, 1, (255, 255, 255)), (10, 10))

        pg.display.flip()
        clock.tick(FPS)
pg.quit()
