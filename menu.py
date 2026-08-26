import pygame
from pathlib import Path
from constants import *
from buttons import Button, ImageButton, MenuButton



class Menu:
    def __init__(self, window):
        w = window.get_width()
        h = window.get_height()

        #Button Dimensions
        button_x = int(w * MENU_BUTTON_X)
        button_width = int(w * MENU_BUTTON_WIDTH)
        button_height = int(h * MENU_BUTTON_HEIGHT)
        first_button_y = int(h * MENU_FIRST_BUTTON_Y)
        button_gap = int(h * MENU_BUTTON_GAP)

        assets_path = Path(__file__).parent / "assets"

        red_paddle_image = pygame.image.load(assets_path / "paddle_red_matte.png").convert_alpha()
        green_paddle_image = pygame.image.load(assets_path / "paddle_green_matte.png").convert_alpha()
        puck_image = pygame.image.load(assets_path / "puck_blue_matte.png").convert_alpha()

        
        self.practice_button = MenuButton("Practice", button_x, first_button_y, button_width, button_height, [red_paddle_image, puck_image])
        self.local_button = MenuButton("Local", button_x, first_button_y + button_height + button_gap, button_width, button_height, [red_paddle_image, puck_image, green_paddle_image])
        self.multiplayer_button = MenuButton("Multiplayer", button_x, first_button_y + (button_height + button_gap) * 2, button_width, button_height, [red_paddle_image, puck_image, green_paddle_image])

      
        self.artwork_rect = pygame.Rect(
            int(w * MENU_ARTWORK_X),
            int(h * MENU_ARTWORK_Y),
            int(w * MENU_ARTWORK_WIDTH),
            int(h * MENU_ARTWORK_HEIGHT),
        )

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

        window.fill(MENU_BACKGROUND_COLOR)

        rink_margin_x = int(w * MENU_RINK_MARGIN_X)
        rink_margin_y = int(h * MENU_RINK_MARGIN_Y)

        rink_rect = pygame.Rect(rink_margin_x, rink_margin_y, w - rink_margin_x * 2, h - rink_margin_y * 2)
        pygame.draw.rect(window, MENU_RINK_LINE_COLOR, rink_rect, width=MENU_RINK_BORDER_WIDTH, border_radius=MENU_RINK_BORDER_RADIUS)

        center_x = w // 2
        center_y = h // 2

        pygame.draw.line(window, MENU_RINK_LINE_COLOR, (center_x, rink_rect.top), (center_x, rink_rect.bottom), width=2)
        pygame.draw.circle(window, MENU_RINK_LINE_COLOR, (center_x, center_y), int(h * 0.18), width=2)

        goal_width = int(w * MENU_GOAL_WIDTH)
        goal_height = int(h * MENU_GOAL_HEIGHT)
        goal_y = int(h * MENU_GOAL_Y)

        left_goal_rect = pygame.Rect(rink_rect.left, goal_y, goal_width, goal_height)
        right_goal_rect = pygame.Rect(rink_rect.right - goal_width, goal_y, goal_width, goal_height)

        pygame.draw.rect(window, RED, left_goal_rect, width=MENU_GOAL_BORDER_WIDTH)
        pygame.draw.rect(window, GREEN, right_goal_rect, width=MENU_GOAL_BORDER_WIDTH)

        pygame.draw.rect(window, GRAY, self.artwork_rect, border_radius=MENU_ARTWORK_BORDER_RADIUS)
        pygame.draw.rect(window, WHITE, self.artwork_rect, width=MENU_ARTWORK_BORDER_WIDTH, border_radius=MENU_ARTWORK_BORDER_RADIUS)

        self.practice_button.draw_button(window)
        self.local_button.draw_button(window)
        self.multiplayer_button.draw_button(window)

        font_size = max(36, int(h * MENU_TITLE_FONT_SCALE))
        font = pygame.font.Font(None, font_size)
        title = font.render("AIR HOCKEY", True, WHITE)
        window.blit(title, title.get_rect(left=int(w * MENU_TITLE_X), top=int(h * MENU_TITLE_Y)))

        self.settings_button.draw_button(window)
