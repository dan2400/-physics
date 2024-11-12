from init import *
import math


class Leaver_sprite_mass(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(lever_sprite)
        self.pos = (width // 2, height // 2)
        self.image = pg.Surface((2 * RADIUS + 100, 2 * RADIUS + 100),
                                        pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color(PLAYER_COLOR),
                               (RADIUS, RADIUS), RADIUS)
        self.font = pg.font.Font(None, 50)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.degree = 60
        self.rect.x = width
        self.rect.y = 0
        self.speed = 0 * time_t
        self.image.blit(self.font.render(str(round(self.speed / time_t, 2)), 0.1, (0, 0, 255)), (10, 0))
        self.tiks = 0

    def update(self):
        global time_t_1
        self.rect.move_ip(self.speed * 100 * math.cos(self.degree), self.speed * 100 * math.sin(self.degree) * -1)
        self.speed += (108 / FPS ** 2) * time_t
        self.image.fill((0, 0, 0))
        pg.draw.circle(self.image, pg.Color(PLAYER_COLOR),
                               (RADIUS, RADIUS), RADIUS)
        self.image.blit(self.font.render(str(round(self.speed / time_t, 2)), 0.1, (0, 0, 255)), (10, 0))
        if self.rect.x < 0 or len(lever_sprite) > 1:
            self.kill()
            time_t_1 = str(self.tiks / FPS)
        self.tiks += 1
        screen.blit(self.font.render(str(self.tiks / FPS), 1, (255, 255, 255)), (width - 100, 10))

