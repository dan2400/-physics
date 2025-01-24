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
import pymunk.pygame_util
from random import randrange

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
        self.start = Button("Начать", 0.3, "black", self.name)
        self.repit = Button("Повторить", 0.6, "black", self.name)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors["red"])
        self.start.draw_but(screen)
        self.repit.draw_but(screen)

    # def new_game(self):
    #     global all_scenes
    #     all_scenes["game"] = Game()
    #     # self.game = Lever()

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start.push():
                self.start.prepare(screen)
            if self.repit.push():
                self.repit.prepare(screen)

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if self.start.push():
                # self.new_game()
                os.environ["STATUS"] = "choice"
                all_scenes['choice'].main()
                os.environ["FROM"] = self.name
            if self.repit.push():
                os.environ["STATUS"] = "choice"
                all_scenes['choice'].repit()
                os.environ["FROM"] = "main"

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "settings"

class Settings(pg.sprite.Sprite):
    def __init__(self, where='choice'):
        self.name = "settings"
        self.game = None
        self.contin = Button("Продолжить", 0.3, "black", self.name)
        self.menu = Button("Меню", 0.6, "black", self.name)
        self.qute = Button("Выйти", 0.9, "black", self.name)
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
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = self.where
            elif self.menu.push():
                os.environ["FROM"] = self.name
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
        global space
        self.name = "lever"
        self.game = None
        self.time = 0
        self.segment_shape = pymunk.Segment(space.static_body, (-20, (height * scale_y) // 3), ((width * scale_x), (height * scale_y) // 3 * 2), 50)
        space.add(self.segment_shape)
        self.segment_shape.elasticity = 0.4
        self.segment_shape.friction = 1.0
        self.current_speed = None

    def __str__(self):
        return self.name

    def create_obj(self, pos):
        circle_mass, circle_size = 1, (0, 30 * scale_y)
        obj_moment = pymunk.moment_for_circle(circle_mass, circle_size[0], circle_size[1])
        obj_body = pymunk.Body(circle_mass, obj_moment)
        obj_body.position = pos
        obj_shape = pymunk.Circle(obj_body, circle_size[1])
        obj_shape.elasticity = 0.8
        obj_shape.friction = 1.0
        obj_shape.color = [randrange(256) for i in range(4)]
        self.current_speed = obj_body
        self.time = time.time()
        space.add(obj_body, obj_shape)


    def speed(self):
        if self.current_speed is None:
            return 0
        return round((self.current_speed.velocity[0] ** 2 + self.current_speed.velocity[1] ** 2) ** 0.5 / 392, 2)


    def draw(self):
        screen.fill(colors["black"])
        space.step(1 / FPS)
        space.debug_draw(draw_o)
        print(self.speed())
        if self.current_speed is not None:
            if int(self.current_speed.position[0]) > width * scale_x - 20:
                self.time = round(time.time() - self.time, 1)
                all_scenes["lever_question"].add_question(self.time)
                all_scenes["lever_question"].add_question_a(self.time)
                self.time = 0
                self.current_speed = None
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "lever_question"


        # lever_sprite.update()
        # lever_sprite.draw(screen)
        # pg.draw.line(screen, colors['green'], [(width * scale_x), RADIUS * 2], [0, 300 * scale_y + RADIUS * 2], 5)
        text = 'ENTER для продолжения'
        text_font = pg.font.Font(None, 50)
        screen.blit(text_font.render(text, 1, (255, 255, 255)), (10, (height * scale_y) - 50 * scale_y))
        text = f'{self.speed()}'
        text_font = pg.font.Font(None, 50)
        screen.blit(text_font.render(text, 1, (255, 255, 255)), (width * scale_x - 100 * scale_x, (height * scale_y) - 50 * scale_y))

    def mouse_button_up(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            Leaver_sprite_mass()

    def mouse_button_down(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.create_obj(event.pos)


    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "lever_question"
            elif event.key == pg.K_ESCAPE:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "settings"


class Content:
    def __init__(self, content):
        self.content = content.split('\n')
        self.delta = 0
        self.name = "content"
        self.game = None
        self.font = pg.font.Font(None, 100)
        self.font_2 = pg.font.Font(None, 50)
        self.window = pg.Surface(((width * scale_x), (height * scale_y - (120 * scale_y))))

    def _mult_line(self, text):
        text = text
        for i in range(len(text)):
            text_temp = self.font_2.render(text[i], 1, (0, 0, 0))
            self.window.blit(text_temp, text_temp.get_rect(center=((width * scale_x) // 2, 50 * scale_y + ((i + self.delta) * 15 * scale_y))))

    def draw(self):
        self.window.fill(colors['white'])
        self._mult_line(self.content)
        screen.blit(self.window, self.window.get_rect(center=((width * scale_x) // 2, (height * scale_y) // 2 - 10 * scale_y)))


class Lever_text(pg.sprite.Sprite):
    def __init__(self):
        self.name = 'lever_text'
        self.game = None
        self.buttons = {
            "lever": Button("Дальше", 0.9, "black", self.name),
        }
        self.font = pg.font.Font(None, 100)
        self.font_2 = pg.font.Font(None, 50)
        self.content = """Ускорение - физическая величина, характеризирующая изменение скорости за единицу времени: [a]=1м/с^2.
            Формула ускорения:
            a = v - v0 / t
            где: a - ускорение, м/с^2; v - скорость, м/с; v0 - начальная скорость, м/с; t - время, с.
            Равноускоренное движение — это движение с постоянным ускорением: а = const.
            Мгновенная скорость — это скорость движущегося объекта в данный момент времени
            Формула мгновенной скорости:
            v = v0 + at
            где: v - скорость, м/с; v0 - начальная скорость, м/с; a - ускорение, м/с^2; t - время, с.
            """
        self.cont = Content(self.content)

    def __str__(self):
        return self.name

    def draw(self):
        screen.fill(colors['white'])
        t1 = self.font.render('Лабораторная работа 1. Ускорение', 1, (0, 0, 0))
        screen.blit(t1, t1.get_rect(center=((width * scale_x) // 2, 70)))
        # num_surf = pg.image.load('lever1.png')
        # num_rect = num_surf.get_rect(center=((width * scale_x) // 2, height // 2 + 50))
        # screen.blit(num_surf, num_rect)
        self.cont.draw()
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
                    os.environ["FROM"] = self.name
                    os.environ["STATUS"] = "lever"
                    break

    def mouse_wheel(self, event):
        if event.type == pg.MOUSEWHEEL:
            match event.y:
                case 1:
                    if self.cont.delta * 50 < height * scale_y:
                        self.cont.delta += 1
                case -1:
                    if self.cont.delta * 50 * scale_y > 0:
                        self.cont.delta -= 1

    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "settings"


class Question:
    def __init__(self, text, right_answer):
        self.name = 'lever_questions'
        self.game = None
        self.font = pg.font.Font(None, 70)
        self.window = pg.Surface(((width * scale_x), (height * scale_y)))
        self.right_answer = right_answer
        self.text = text.split('\n')

    def _mult_line(self, text):
        text = text
        for i in range(len(text)):
            text_temp = self.font.render(text[i], 1, (0, 0, 0))
            self.window.blit(text_temp, text_temp.get_rect(center=((width * scale_x) // 2, (height * scale_y) // 5 + ((i) * 50))))

    def draw(self):
        self.window.fill(colors['white'])
        self._mult_line(self.text)

        screen.blit(self.window, self.window.get_rect(center=((width * scale_x) // 2, (height * scale_y) // 2 + 50 * scale_y)))


class Lever_question(pg.sprite.Sprite):
    def __init__(self):
        self.res = 0
        self.ok = 0
        self.russian_name = "Ускорение"
        self.name = 'lever_question'
        self.game = None
        self.input = InputBox((width * scale_x) // 2, height - 230, screen, True)
        self.buttons = {
            "lever": Button("Ответить", 0.9, "black", self.name),
        }
        self.font = pg.font.Font(None, 70)
        self.questions = [
            Question(f"{1}\nфизическая векторная величина,\n характеризующая быстроту изменения скорости тела \n", "ускорение"),

        ]
        self.id = 1

    def __str__(self):
        return self.name

    def add_question(self, time):
        self.questions.append(Question(f"{len(self.questions) + 1}\nУкажите скорость мячика на в конце пути\nВремя в среднем: {time} c.\nУскорение: 5 м/с^2.\n", str(round(time * 5))))

    def add_question_a(self, time):
        self.questions.append(Question(f"{len(self.questions) + 1}\nУкажите ускорение мячика\nВремя в среднем: {time} c.\nСкорость в конце: {round(time * 5)} м/с.\n", "5"))

    def res(self, res):
        self.res = res

    def draw(self):
        screen.fill(colors['white'])
        self.questions[self.id - 1].draw()
        self.input.draw()
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
                    if self.input.out() == self.questions[self.id - 1].right_answer.lower():
                        self.ok += 1
                        screen.fill(colors['green'])
                        t1 = self.font.render('Верно', 1, (255, 255, 255))
                        screen.blit(t1, t1.get_rect(center=((width * scale_x) // 2, 70)))
                    elif self.input.out() != self.questions[self.id - 1].right_answer.lower():
                        screen.fill(colors['red'])
                        t1 = self.font.render('Ошибка', 1, (255, 255, 255))
                        screen.blit(t1, t1.get_rect(center=((width * scale_x) // 2, 70)))
                    self.input.clear()
                    pygame.display.flip()
                    time.sleep(2)
                    if self.id == len(self.questions):
                        string = f"{os.environ.get("STATUS", default="menu")} {str(self.russian_name)} {str(int(round(self.ok / self.id, 2) * 100))} \n"
                        with open("repit.txt", "a+") as f:
                            if not (string in f.readlines()):
                                f.write(string)
                        self.id = 1
                        self.questions = [
                            Question(f"{1}\nфизическая векторная величина,\n характеризующая быстроту изменения скорости тела \n", "ускорение"),

                        ]
                        os.environ["STATUS"] = "menu"
                    else:
                        self.id += 1

    def key_down(self, event):
        self.input.enter(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "settings"


class Choice(pg.sprite.Sprite):
    def __init__(self):
        self.name = "choice"
        self.game = None

        self.buttons = {}

    def __str__(self):
        return self.name

    def repit(self):
        self.buttons = {}
        try:
            with open("repit.txt", "r") as f:
                k = f.readlines()
                if len(k) == 0:
                    os.environ["FROM"] = self.name
                    os.environ["STATUS"] = "menu"
                    return
                for line in k:
                    temp = line.split(' ')
                    self.buttons[temp[0]] = Button(temp[1], 0.3 * (len(self.buttons) + 1), "black", self.name, ok=float(temp[2]))
        except FileNotFoundError as er:
            print(er)
            os.environ["FROM"] = self.name
            os.environ["STATUS"] = "menu"


    def main(self):
        self.buttons = {
            "lever": Button("Ускорение", 0.3, "black", self.name),
        }

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
            for name, button in self.buttons.items():
                print(name, button.push())
                if button.push():
                    if name == "lever" or name == "lever_question":
                        os.environ["FROM"] = self.name
                        os.environ["STATUS"] = "lever_text"


    def key_down(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                os.environ["FROM"] = self.name
                os.environ["STATUS"] = "menu"


if __name__ == '__main__':
    themes = [
        'lever',
    ]
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
                all_scenes["lever"].mouse_button_down(event)

            if os.environ.get("STATUS", default="main") == "menu":
                all_scenes["menu"].draw()
                all_scenes["menu"].mouse_button_down(event)
                all_scenes["menu"].mouse_button_up(event)
                all_scenes["menu"].key_down(event)

            if os.environ.get("STATUS", default="main") == "lever_text":
                all_scenes["lever_text"].mouse_button_up(event)
                all_scenes["lever_text"].mouse_button_down(event)
                all_scenes["lever_text"].mouse_wheel(event)
                all_scenes["lever_text"].draw()

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

# 5 true