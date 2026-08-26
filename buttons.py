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

class MenuButton(Button):
    def __init__(self, text, x, y, width, height, images):
        super().__init__(text, x, y, width, height, bg_color=GRAY, text_color=WHITE)
        image_size = int(height * 0.5)
        self.images = [pygame.transform.smoothscale(image, (image_size, image_size))
                       for image in images]

    def draw_button(self, window):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        background_color = LIGHT_GRAY if hovered else self.bg_color
        text_color = BLACK if hovered else self.text_color

        #Button Background
        pygame.draw.rect(window, background_color, self.rect, border_radius=10)
        accent_rect = pygame.Rect(self.rect.left, self.rect.top, 6, self.rect.height)
        pygame.draw.rect(window, BLUE, accent_rect, border_radius=10)

        #Left aligned labeling
        font_size = max(12, int(self.rect.height * 0.45))
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 20, self.rect.centery))
        window.blit(text_surface, text_rect)

        #Images begin on right side of button
        image_gap = 4
        image_x = self.rect.right - 15

        for image in reversed(self.images):
            image_rect = image.get_rect(midright=(image_x, self.rect.centery))
            window.blit(image, image_rect)
            image_x = image_rect.left - image_gap

class ImageButton:
    def __init__(self, image, x, y, width, height):
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw_button(self, window):
        window.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class OptionButton(Button):
    def __init__(self, text, x, y, width, height):
        super().__init__(
            text,
            x,
            y,
            width,
            height,
            bg_color=BLACK,
            text_color=WHITE,
        )

        self.selected = False

    def draw_button(self, window):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        if self.selected:
            background_color = GOLD
            text_color = BLACK
        elif hovered:
            background_color = LIGHT_GRAY
            text_color = BLACK
        else:
            background_color = BLACK
            text_color = WHITE

        pygame.draw.rect(window, background_color, self.rect, border_radius=10)
        pygame.draw.rect(window, WHITE, self.rect, width=2, border_radius=10)

        font_size = max(12, int(self.rect.height * 0.5))
        font = pygame.font.Font(None, font_size)
        text = font.render(self.text, True, text_color)

        window.blit(text, text.get_rect(center=self.rect.center))

            



            
