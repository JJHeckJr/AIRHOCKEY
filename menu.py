import pygame
from constants import *
from buttons import Button

class Menu:
    def __init__(self, window):
        w = window.get_width()
        h = window.get_height()
        button_width = int(w * .25)
        button_height = int(h * .08)
        center_x = w // 2 - button_width // 2

        self.practice_button = Button("Practice", center_x, int(h * 0.4), button_width, button_height)
        self.local_button = Button("Local", center_x, int(h * 0.52), button_width, button_height)
        self.multiplayer_button = Button("Multiplayer", center_x, int(h * 0.64), button_width, button_height)

    def draw_menu(self, window):
        w = window.get_width()
        h = window.get_height()

        self.practice_button.draw_button(window)
        self.local_button.draw_button(window)
        self.multiplayer_button.draw_button(window)

        font_size = max(36, int(h * 0.15))
        font = pygame.font.Font(None, font_size)
        title = font.render("Welcome to Air Hockey!", True, WHITE)
        window.blit(title, title.get_rect(center=(w // 2, int(h * .15))))
