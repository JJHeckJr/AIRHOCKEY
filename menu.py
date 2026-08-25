import pygame
from pathlib import Path
from constants import *
from buttons import Button, ImageButton



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

        #loading settings image than creating a new surface with the desired size
        icon_path = (Path(__file__).parent / "assets" / "settings_icon.png")
        self.settings_initial = pygame.image.load(icon_path).convert_alpha()
        self.settings_button = ImageButton(
        self.settings_initial, 
        w - SETTINGS_ICON_SIZE - SETTINGS_ICON_MARGIN, 
        SETTINGS_ICON_MARGIN, SETTINGS_ICON_SIZE, 
        SETTINGS_ICON_SIZE)


    def handle_ui_events(self, event):
        if self.practice_button.is_clicked(event):
            return PRACTICE
        if self.local_button.is_clicked(event):
            return LOCAL_MENU
        if self.multiplayer_button.is_clicked(event):
            return MULTIPLAYER
        if self.settings_button.is_clicked(event):
            return SETTINGS
        return None

    def update(self):
        pass
    
    def draw(self, window):
        w = window.get_width()
        h = window.get_height()

        self.practice_button.draw_button(window)
        self.local_button.draw_button(window)
        self.multiplayer_button.draw_button(window)
        self.settings_button.draw_button(window)

        font_size = max(36, int(h * 0.15))
        font = pygame.font.Font(None, font_size)
        title = font.render("Welcome to Air Hockey!", True, WHITE)
        window.blit(title, title.get_rect(center=(w // 2, int(h * .15))))
