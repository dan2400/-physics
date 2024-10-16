from init import *



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
        mouse_x, mouse_y = pg.mouse.get_pos()
        self.rect.x = mouse_x
        self.rect.y = mouse_y
        self.speed = 0 * time
        self.image.blit(self.font.render(str(round(self.speed / time, 2)), 0.1, (0, 0, 255)), (10, 0))

    def update(self):
        self.rect.move_ip(0, self.speed * 100)
        self.speed += (108 / FPS ** 2) * time
        self.image.fill((0, 0, 0))
        pg.draw.circle(self.image, pg.Color(PLAYER_COLOR),
                               (RADIUS, RADIUS), RADIUS)
        self.image.blit(self.font.render(str(round(self.speed / time, 2)), 0.1, (0, 0, 255)), (10, 0))
        if self.rect.y > height:
            self.kill()
