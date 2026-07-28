import pygame
from constants import *
from buttons import Button


class LocalMenu:
    def __init__(self, window):
        w = window.get_width()
        h = window.get_height()
        button_width = int(w * .25)
        button_height = int(h * .08)
        gap = 20

        left_x = w // 2 - button_width - gap // 2
        right_x = w // 2 + gap // 2
        back_width = button_width + gap
        back_x = w // 2 - back_width // 2

        self.cpu_button = Button("User vs CPU", left_x, int(h * 0.4), button_width, button_height)
        self.user_button = Button("User vs User", right_x, int(h * 0.4), button_width, button_height)
        self.back_button = Button("<- Back", back_x, int(h * 0.52), back_width, button_height, border_only=True, text_color=WHITE)

    def draw_local_menu(self, window):
        self.cpu_button.draw_button(window)
        self.user_button.draw_button(window)
        self.back_button.draw_button(window)


    
    
