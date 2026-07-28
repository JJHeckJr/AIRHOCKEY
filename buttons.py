import pygame
from constants import *


class Button:
    def __init__(self, text, x, y, width, height, bg_color = WHITE, text_color=BLACK, border_only=False):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_only = border_only

    def draw_button(self, window):
        #Gettinig our mouse position
        mouse_pos = pygame.mouse.get_pos()
        if self.border_only:
            if self.rect.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                hover_surface.fill((255, 255, 255, 150))
                window.blit(hover_surface, self.rect.topleft)
            pygame.draw.rect(window, self.bg_color, self.rect, 2)
        else:
            color = LIGHT_GRAY if self.rect.collidepoint(mouse_pos) else self.bg_color
            pygame.draw.rect(window, color, self.rect)

        font_size = max(12, int(self.rect.height * 0.5))
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(self.text, True, self.text_color)
        window.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
            
