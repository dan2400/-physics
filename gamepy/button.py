from init import *
import os


class Button:
    def __init__(self, text, step, color="white", scene="main"):
        self.scene = scene
        self.step = step
        self.Color = pg.Color(color)
        font = pg.font.Font(None, int(150 * scale_x))
        self.text_out = text
        self.text = font.render(text, True, self.Color)
        self.text_x = width - (int(width // 2)) - self.text.get_width() // 2
        self.text_y = int(height * step * scale_y) - self.text.get_height() // 2
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()
        self.width = 2

    def __str__(self):
        return f"Button(text='{self.text_out}', step={self.step}, color='{self.Color}', scene='{self.scene}')"

    def draw_but(self, screen_in):
        screen_in.blit(self.text, (self.text_x, self.text_y))
        pg.draw.rect(screen_in, self.Color,
                         (width * 0.5 - width * 0.1 - int(20 * scale_x), self.text_y - int(20 * scale_y),
                          width * 0.2 + int(40 * scale_x), self.text_h + int(40 * scale_y)),
                     int(self.width * scale_y), 50, 20)

    def push(self):
        print(f"{self.scene} == {os.environ.get('STATUS', default='main')}")
        if self.scene == os.environ.get("STATUS", default="main"):
            x, y = pg.mouse.get_pos()
            min_x = width * 0.5 - width * 0.1 - int(20 * scale_x)
            max_x = min_x + width * 0.2 + int(40 * scale_x)
            min_y = self.text_y - int(20 * scale_y)
            max_y = min_y + self.text_h + int(40 * scale_y)
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
            else:
                return False

    def prepare(self, screen_in):
        x, y = pg.mouse.get_pos()
        min_x = width * 0.5 - width * 0.1 - int(20 * scale_x)
        max_x = min_x + width * 0.2 + int(40 * scale_x)
        min_y = self.text_y - int(20 * scale_y)
        max_y = min_y + self.text_h + int(40 * scale_y)
        if min_x <= x <= max_x and min_y <= y <= max_y:
            width_new = 5
            Color = tuple(map(lambda x: x + 50 if x != 255 else 255, list(self.Color)))
            screen_in.blit(self.text, (self.text_x, self.text_y))
            pg.draw.rect(screen_in, Color,
                         (width * 0.5 - width * 0.1 - int(20 * scale_x), self.text_y - int(20 * scale_y),
                          width * 0.2 + int(40 * scale_x), self.text_h + int(40 * scale_y)),
                         int(width_new * scale_y), 50, 20)

