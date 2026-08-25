import pygame

from buttons import Button, OptionButton
from constants import *

class GameSettings:
    def __init__(self):
        self.cpu_difficulty = "normal"  # Default difficulty
        self.win_condition = "time" # Default win condition
        self.match_minutes = 3 # Default match duration in minutes
        self.target_score = 7 # Default target score

class SettingsMenu:
    def __init__(self, window, game_settings):
        self.game_settings = game_settings

        w = window.get_width()
        h = window.get_height()

        self.panel_rect = pygame.Rect(
        w // 2 - SETTINGS_PANEL_WIDTH // 2, int(h * 0.2),
        SETTINGS_PANEL_WIDTH, SETTINGS_PANEL_HEIGHT)           

        #layout for difficulty buttons
        total_width = (SETTINGS_OPTION_BUTTON_WIDTH * 3 + SETTINGS_OPTION_GAP * 2)
        self.difficulty_y = self.panel_rect.top + SETTINGS_DIFFICULTY_ROW_Y
        difficulty_x = (self.panel_rect.centerx - total_width // 2)

        self.difficulty_buttons = {
            "easy": OptionButton(
            "Easy",
            difficulty_x,
            self.difficulty_y,
            SETTINGS_OPTION_BUTTON_WIDTH,
            SETTINGS_OPTION_BUTTON_HEIGHT,
            ),
            "normal": OptionButton(
            "Normal",
            difficulty_x + SETTINGS_OPTION_BUTTON_WIDTH + SETTINGS_OPTION_GAP,
            self.difficulty_y,
            SETTINGS_OPTION_BUTTON_WIDTH,
            SETTINGS_OPTION_BUTTON_HEIGHT,
            ),
            "hard": OptionButton(
            "Hard",
            difficulty_x + (SETTINGS_OPTION_BUTTON_WIDTH + SETTINGS_OPTION_GAP) * 2,
            self.difficulty_y,
            SETTINGS_OPTION_BUTTON_WIDTH,
            SETTINGS_OPTION_BUTTON_HEIGHT
            ),
        }

        # Win-condition row position
        self.condition_y = (self.panel_rect.top + SETTINGS_WIN_CONDITION_ROW_Y)
        condition_width = (SETTINGS_OPTION_BUTTON_WIDTH * 2 + SETTINGS_OPTION_GAP)
        condition_x = (self.panel_rect.centerx - condition_width // 2)

        self.win_conditions_buttons = {
            "time": OptionButton(
                "Timed Match",
                condition_x,
                self.condition_y,
                SETTINGS_OPTION_BUTTON_WIDTH,
                SETTINGS_OPTION_BUTTON_HEIGHT,
            ),
            "score": OptionButton(
                "First to 7",
                condition_x + SETTINGS_OPTION_BUTTON_WIDTH + SETTINGS_OPTION_GAP,
                self.condition_y,
                SETTINGS_OPTION_BUTTON_WIDTH,
                SETTINGS_OPTION_BUTTON_HEIGHT,
            ),
        }

        self.match_length_y = (self.panel_rect.top + SETTINGS_MATCH_LENGTH_ROW_Y)
        self.decrease_minutes_button = OptionButton(
        "<", 
        self.panel_rect.centerx - SETTINGS_MINUTE_TEXT_WIDTH // 2 - SETTINGS_OPTION_GAP - SETTINGS_ARROW_BUTTON_SIZE,
        self.match_length_y, 
        SETTINGS_ARROW_BUTTON_SIZE, 
        SETTINGS_ARROW_BUTTON_SIZE)

        self.increase_minutes_button = OptionButton(
        ">",
        self.panel_rect.centerx
        + SETTINGS_MINUTE_TEXT_WIDTH // 2
        + SETTINGS_OPTION_GAP,
        self.match_length_y,
        SETTINGS_ARROW_BUTTON_SIZE,
        SETTINGS_ARROW_BUTTON_SIZE)


        self.back_button = Button(
        "<- Back", w // 2 - SETTINGS_BACK_BUTTON_WIDTH // 2,
        h - SETTINGS_BACK_BUTTON_HEIGHT - SETTINGS_BACK_BUTTON_MARGIN,
        SETTINGS_BACK_BUTTON_WIDTH,
        SETTINGS_BACK_BUTTON_HEIGHT,
        border_only=True,
        text_color=WHITE) 

    def handle_ui_events(self, event):
        for difficulty, button in self.difficulty_buttons.items():
            if button.is_clicked(event):
                self.game_settings.cpu_difficulty = difficulty

        for condition, button in self.win_conditions_buttons.items():
            if button.is_clicked(event):
                self.game_settings.win_condition = condition

        if self.game_settings.win_condition == "time":
            if self.decrease_minutes_button.is_clicked(event):
                self.game_settings.match_minutes = max(1, self.game_settings.match_minutes - 1)
            if self.increase_minutes_button.is_clicked(event):
                self.game_settings.match_minutes = min(5, self.game_settings.match_minutes + 1)

        if self.back_button.is_clicked(event):
            return MENU

        return None

    def update(self):
        pass

    def draw(self, window):
        w = window.get_width()
        h = window.get_height()

        font = pygame.font.Font(None, SETTINGS_TITLE_FONT_SIZE)
        title = font.render("Settings", True, WHITE)
        title_rect = title.get_rect(center=(w // 2, int(h * 0.1)))

        window.blit(title, title_rect)

        pygame.draw.rect(window, GRAY, self.panel_rect)
        pygame.draw.rect(window, WHITE, self.panel_rect, 2)

        #Difficulty label and buttons
        label_font = pygame.font.Font(None, SETTINGS_LABEL_FONT_SIZE)
        difficulty_label = label_font.render("CPU Difficulty", True, WHITE)
        difficulty_label_rect = difficulty_label.get_rect(midbottom=(self.panel_rect.centerx, self.difficulty_y - SETTINGS_LABEL_GAP))
        window.blit(difficulty_label, difficulty_label_rect)

        for difficulty, button in self.difficulty_buttons.items():
            button.selected = (self.game_settings.cpu_difficulty == difficulty)
            button.draw_button(window)

        condition_label = label_font.render("Win Condition", True, WHITE)
        condition_label_rect = condition_label.get_rect(midbottom=(self.panel_rect.centerx, self.condition_y - SETTINGS_LABEL_GAP))
        window.blit(condition_label, condition_label_rect)

        #Win-condition-buttons
        for condition, button in self.win_conditions_buttons.items():
            button.selected = (self.game_settings.win_condition == condition)
            button.draw_button(window)

        if self.game_settings.win_condition == "time":
            match_length_label = label_font.render("Match Length", True, WHITE)
            match_length_label_rect = match_length_label.get_rect(midbottom=(self.panel_rect.centerx, self.match_length_y - SETTINGS_LABEL_GAP))
            window.blit(match_length_label, match_length_label_rect)

            minutes = self.game_settings.match_minutes
            minute_word = "minute" if minutes == 1 else "minutes"
            minutes_text = label_font.render(f"{minutes} {minute_word}", True, WHITE)
            minutes_rect = minutes_text.get_rect(center=(self.panel_rect.centerx, self.match_length_y + SETTINGS_ARROW_BUTTON_SIZE // 2))
            window.blit(minutes_text, minutes_rect)
            self.decrease_minutes_button.draw_button(window)
            self.increase_minutes_button.draw_button(window)
            
        self.back_button.draw_button(window)
