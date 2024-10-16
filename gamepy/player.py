from init import *



class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.pos = (width // 2, height // 2)
        self.image = pg.Surface((2 * RADIUS, 2 * RADIUS),
                                        pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color(PLAYER_COLOR),
                               (RADIUS, RADIUS), RADIUS)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.speed = int(150 * scale_y)

    def update(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        distance = int(math.dist((mouse_x, mouse_y), (self.rect.centerx, self.rect.centery)))
        if distance >= self.speed:
            self.rect.move_ip((self.speed * dx) / distance, (self.speed * dy) / distance)
        else:
            self.rect.center = pg.mouse.get_pos()
