from init import *
import os


class Button:
    def __init__(self, text, step, color="white", scene="main", ok=0):
        self.scene = scene
        self.step = step
        self.Color = pg.Color(color)
        font = pg.font.Font(None, int(50 * scale_x))
        self.text_out = text
        self.text = font.render(text, True, self.Color)
        self.text_s_1000000 = font.render("Нажми на меня!", True, self.Color)
        self.text_x = int(width * scale_x // 2) - self.text.get_width() // 2
        self.text_y = int(height * step * scale_y) - self.text.get_height() // 2
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()
        self.width = 2
        self.ok = ok
        self.count = 0

    def __str__(self):
        return f"Button(text='{self.text_out}', step={self.step}, color='{self.Color}', scene='{self.scene}')"

    def prepare(self, screen_in):
        x, y = pg.mouse.get_pos()
        min_x = (width * scale_x) * 0.5 - (width * scale_x) * 0.1 - int(20 * scale_x)
        max_x = min_x + (width * scale_x) * 0.2 + int(40 * scale_x)
        min_y = self.text_y - int(20 * scale_y)
        max_y = min_y + self.text_h + int(40 * scale_y)
        if min_x <= x <= max_x and min_y <= y <= max_y:
            width_new = 5
            Color = tuple(map(lambda x: 255 if x != 255 else 0, list(self.Color)))
            screen_in.blit(self.text, (self.text_x, self.text_y))
            pg.draw.rect(screen_in, Color,
                         ((width * scale_x) * 0.5 - (width * scale_x) * 0.1 - int(40 * scale_x), self.text_y - int(20 * scale_y),
                          (width * scale_x) * 0.2 + int(80 * scale_x), self.text_h + int(40 * scale_y)),
                         int(width_new * scale_y), 50, 20)
            self.count += 1

    def do_stupid_thing(self, screen_in):
        if self.count >= 10000:
           self.text = self.text_s_1000000

    def prepare_inside(self, screen_in):
        x, y = pg.mouse.get_pos()
        min_x = (width * scale_x) * 0.5 - (width * scale_x) * 0.1 - int(20 * scale_x)
        max_x = min_x + (width * scale_x) * 0.2 + int(40 * scale_x)
        min_y = self.text_y - int(20 * scale_y)
        max_y = min_y + self.text_h + int(40 * scale_y)
        if min_x <= x <= max_x and min_y <= y <= max_y:
            width_new = 5
            delta = 25
            Color = tuple(map(lambda x: x + delta if x <= 255 - delta else 255, list(self.Color)))
            screen_in.blit(self.text, (self.text_x, self.text_y))
            pg.draw.rect(screen_in, Color,
                         ((width * scale_x) * 0.5 - (width * scale_x) * 0.1 - int(40 * scale_x), self.text_y - int(20 * scale_y),
                          (width * scale_x) * 0.2 + int(80 * scale_x), self.text_h + int(40 * scale_y)),
                         int(width_new * scale_y), 50, 20)
            self.count += 1

    def draw_but(self, screen_in):
        if self.ok != 0:
            pg.draw.rect(screen_in, "#008D00",
                         ((width * scale_x) // 2 - (width * scale_x) // 10 - int(40 * scale_x), self.text_y - int(20 * scale_y),
                          (((width * scale_x) // 5 + int(80 * scale_x)) * (self.ok / 100)), self.text_h + int(40 * scale_y)), border_radius=50, border_top_left_radius=20)
        screen_in.blit(self.text, (self.text_x, self.text_y))
        pg.draw.rect(screen_in, self.Color,
                         ((width * scale_x) // 2 - (width * scale_x) // 10 - int(40 * scale_x), self.text_y - int(20 * scale_y),
                          (width * scale_x) // 5 + int(80 * scale_x), self.text_h + int(40 * scale_y)),
                     int(self.width * scale_y), 50, 20)
        self.prepare_inside(screen_in)
        print(self.count)
        self.do_stupid_thing(screen_in)

    def push(self):
        if self.scene == os.environ.get("STATUS", default="main"):
            x, y = pg.mouse.get_pos()
            min_x = (width * scale_x) * 0.5 - (width * scale_x) * 0.1 - int(20 * scale_x)
            max_x = min_x + (width * scale_x) * 0.2 + int(40 * scale_x)
            min_y = self.text_y - int(20 * scale_y)
            max_y = min_y + self.text_h + int(40 * scale_y)
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
            else:
                return False


class Window:
    def __init__(self, title, size=(width, height), color="white", name="main"):
        self.name = name
        self.title = title
        self.size = size
        self.color = pg.Color(color)
        self.screen = pg.display.set_mode(size)
        self.screen.fill(self.color)
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.buttons = []
        self.text = []
        self.images = []
        self.rectangles = []
        self.lines = []
        self.circles = []