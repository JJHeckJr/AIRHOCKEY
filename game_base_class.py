import pygame
from buttons import Button
from constants import *
from puck import Puck
from rink import Rink
from scoreboard import Scoreboard

class GameBaseMode:
    def __init__(self, window):
        self.rink = Rink(window)
        self.puck = Puck(self.rink)
        self.paused_game = False
        self.menu_button = Button("Main Menu", 0, 0, PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT)
        self.rematch_button = Button("Rematch", 0, 0, PAUSE_MENU_BUTTON_WIDTH, PAUSE_MENU_BUTTON_HEIGHT)
        self.flash_goal = None
        self.flash_timer = 0
        self.scoreboard = Scoreboard()
        self.match_over = False

    def handle_ui_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.paused_game = not self.paused_game
        if self.paused_game and self.menu_button.is_clicked(event):
            self.paused_game = False
        if self.menu_button.is_clicked(event):
            return MENU
        return None

    def on_enter(self):
        self.reset_match()

    def reset_match(self):
        self.scoreboard.reset_score()
        self.paused_game = False
        self.flash_goal = None
        self.flash_timer = 0
    
    def _update_flash(self):
        goal = self.puck.check_scored_goal(self.rink)
        if goal and self.flash_timer == 0:
            self.flash_goal = goal
            self.flash_timer = GOAL_FLASH_DURATION
            self.scoreboard.update_score(goal)
        
        if self.flash_timer > 0:
            if self.flash_timer == 1:
                self._on_goal_reset()
            self.flash_timer -= 1
        else:
            self.flash_goal = None

    def _on_goal_reset(self):
        pass

    def _draw_flash(self, window):
        if self.flash_timer <= 0 or self.flash_timer % 20 >= 10:
            return
        if self.flash_goal == 'top':
            rect = self.rink.top_goal
        elif self.flash_goal == 'bottom':
            rect = self.rink.bottom_goal
        else:
            return
        flash_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        flash_surface.fill((*GOAL_FLASH_COLOR, GOAL_FLASH_ALPHA))
        window.blit(flash_surface, rect.topleft)
    
    def _draw_pause_overlay(self, window):
        if not self.paused_game:
            return
        w, h = window.get_width(), window.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, PAUSE_OVERLAY_ALPHA))
        window.blit(overlay, (0, 0))

        font = pygame.font.Font(None, PAUSE_FONT_SIZE)
        text = font.render("PAUSED", True, WHITE)
        window.blit(text, text.get_rect(center=(w // 2, h // 2 - 40)))

        self.menu_button.rect.center = (w // 2, h // 2 + 30)
        self.menu_button.draw_button(window)

    def _draw_winner_overlay(self, window):
        if not self.match_over:
            return
        w, h = window.get_width(), window.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, PAUSE_OVERLAY_ALPHA))
        window.blit(overlay, (0, 0))

        if self.scoreboard.top_score > self.scoreboard.bottom_score:
            message = "BOT WINS"
        elif self.scoreboard.bottom_score > self.scoreboard.top_score:
            message = "TOP Wins"
        else:
            message = "TIE GAME"

        font = pygame.font.Font(None, PAUSE_FONT_SIZE)
        text = font.render(message, True, WHITE)
        window.blit(text, text.get_rect(center=(w // 2, h // 2 - 90)))

        button_gap = 20
        self.rematch_button.rect.center = (w // 2 - (PAUSE_MENU_BUTTON_WIDTH + button_gap) // 2, h // 2 + 60)
        self.menu_button.rect.center =  ( w // 2 + (PAUSE_MENU_BUTTON_WIDTH + button_gap) // 2, h // 2 + 60)
        self.rematch_button.draw_button(window)
        self.menu_button.draw_button(window)

