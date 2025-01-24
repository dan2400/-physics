import pygame
from init import colors


class InputBox:
    def __init__(self, x, y, screen, is_active=False):
        self.x, self.y = x, y
        self.text = ''
        self.font = pygame.font.SysFont(None, 100)
        self.input_active = is_active
        self.screen = screen

    def draw(self):
        text_surf = self.font.render(self.text, True, colors["black"])
        self.screen.blit(text_surf, text_surf.get_rect(center=(self.x, self.y)))

    def activate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.input_active = True

    def enter(self, event):
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                self.input_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text =  self.text[:-1]
            else:
                self.text += event.unicode

    def clear(self):
        self.text = ''

    def out(self):
        print(self.text)
        return self.text
