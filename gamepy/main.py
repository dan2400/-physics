from init import *
from input_box import InputBox
from settings import *
from sprites import *
from button import *
from numba import njit
import dotenv
import os
import texts
import time

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
    def __init__(self, where='choice'):
        self.name = "settings"
        self.game = None
        self.contin = Button("Continue", 0.3, "black", self.name)
        self.menu = Button("Menu", 0.6, "black", self.name)
        self.qute = Button("Qute", 0.9, "black", self.name)
        self.where = where

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["green"])
        self.contin.draw_but(screen)
        self.menu.draw_but(screen)
        self.qute.draw_but(screen)

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.contin.push():
                self.contin.prepare(screen)
            elif self.menu.push():
                self.menu.prepare(screen)
            elif self.qute.push():
                self.qute.prepare(screen)

    def mouse_button_up(self, event):
        global run
        if event.type == pg.MOUSEBUTTONUP:
            if self.contin.push():
                # self.new_game()
                os.environ["STATUS"] = self.where
            elif self.menu.push():
                os.environ["STATUS"] = "menu"
            elif self.qute.push():
                run = False

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                global run
                run = False


class Lever(pg.sprite.Sprite):
    def __init__(self):
        self.name = "lever"
        self.game = None
        self.time = None

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["black"])
        lever_sprite.update()
        lever_sprite.draw(screen)
        pg.draw.line(screen, colors['green'], [width, RADIUS * 2], [0, 598 * scale_y + RADIUS * 2], 5)
        text = 'ENTER для продолжения'
        text_font = pg.font.Font(None, 50)
        screen.blit(text_font.render(text, 1, (255, 255, 255)), (10, height - 450 * scale_y))

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            Leaver_sprite_mass()

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                os.environ["STATUS"] = "lever_question"


class Lever_text(pg.sprite.Sprite):
    def __init__(self):
        self.name = 'lever_text'
        self.game = None
        self.buttons = {
            "lever": Button("Дальше", 0.9, "black", self.name),
        }
        self.font = pg.font.Font(None, 100)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors['white'])
        t1 = self.font.render('Лабораторная работа 1. Ускорение', 1, (0, 0, 0))
        screen.blit(t1, t1.get_rect(center=(width // 2, 70)))
        num_surf = pg.image.load('lever1.png')
        num_rect = num_surf.get_rect(center=(width // 2, height // 2 - 10))
        screen.blit(num_surf, num_rect)
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


class Lever_question(pg.sprite.Sprite):
    def __init__(self):
        self.name = 'lever_question'
        self.game = None
        self.input = InputBox(width // 2, height - 230, screen, True)
        self.buttons = {
            "lever": Button("Ответить", 0.9, "black", self.name),
        }
        self.font = pg.font.Font(None, 70)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors['white'])
        self.input.draw()
        t1 = self.font.render('1.25', 1, (0, 0, 0))
        t2 = self.font.render('Время в среднем: 1.25 c.', 1, (0, 0, 0))
        t3 = self.font.render('Растояние: 3.9 м.', 1, (0, 0, 0))
        screen.blit(t1, t1.get_rect(center=(width // 2, 70)))
        screen.blit(t2, t2.get_rect(center=(width // 2, 150)))
        screen.blit(t3, t3.get_rect(center=(width // 2, 230)))
        for _, button in self.buttons.items():
            button.draw_but(screen)

    def mouse_button_down(self, event):
        self.input.activate(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            for _, button in self.buttons.items():
                if button.push():
                    button.prepare(screen)
                    break

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            for _, button in self.buttons.items():
                if button.push():
                    if self.input.out() == "5":
                        screen.fill(colors['green'])
                        t1 = self.font.render('Верно', 1, (255, 255, 255))
                        screen.blit(t1, t1.get_rect(center=(width // 2, 70)))
                    else:
                        screen.fill(colors['red'])
                        t1 = self.font.render('Ошибка', 1, (255, 255, 255))
                        screen.blit(t1, t1.get_rect(center=(width // 2, 70)))
                    pygame.display.flip()
                    time.sleep(2)
                    os.environ["STATUS"] = "menu"
                    break

    def key_down(self, event):
        self.input.enter(event)


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
                    os.environ["STATUS"] = "lever_text"
                    break

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["STATUS"] = "menu"


if __name__ == '__main__':
    all_scenes = {
        "menu": Menu(),
        "game": Game(),
        "settings": Settings(),
        "lever": Lever(),
        "choice": Choice(),
        "lever_text": Lever_text(),
        "lever_question": Lever_question(),
    }
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if os.environ.get("STATUS", default="main") == "game":
                all_scenes["game"].draw()
                all_scenes["game"].key_down(event)

            if os.environ.get("STATUS", default="main") == "settings":
                all_scenes["settings"].draw()
                all_scenes["settings"].mouse_button_down(event)
                all_scenes["settings"].mouse_button_up(event)
                all_scenes["settings"].key_down(event)

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

            if os.environ.get("STATUS", default="main") == "lever_text":
                all_scenes["lever_text"].draw()
                all_scenes["lever_text"].mouse_button_up(event)
                all_scenes["lever_text"].mouse_button_down(event)

            if os.environ.get("STATUS", default="main") == "lever_question":
                all_scenes["lever_question"].draw()
                all_scenes["lever_question"].key_down(event)
                all_scenes["lever_question"].mouse_button_up(event)
                all_scenes["lever_question"].mouse_button_down(event)

        if os.environ.get("STATUS", default="main") == "lever":
            all_scenes["lever"].draw()


        if show_fps:
            fps = str(int(clock.get_fps()))
            font = pg.font.Font(None, 20)
            screen.blit(font.render(fps, 1, (255, 255, 255)), (10, 10))

        pg.display.flip()
        clock.tick(FPS)
pg.quit()
