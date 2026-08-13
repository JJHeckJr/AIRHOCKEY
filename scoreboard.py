import pygame
from constants import *

class Scoreboard:
    def __init__(self):
        self.top_score = 0
        self.bottom_score = 0

    def update_score(self, goal):
        if goal == 'top':
            self.top_score += 1
        elif goal == 'bottom':
            self.bottom_score += 1
    
    def draw_scoreboard(self, window, rink):
        w = window.get_width()
        center_x = (rink.right + w) // 2
        font = pygame.font.Font(None, SCOREBOARD_FONT_SIZE)
        score_text = font.render(f"BOT {self.top_score} -  TOP {self.bottom_score}", True, WHITE)
        text_rect = score_text.get_rect(midtop=(center_x, SCOREBOARD_OFFSET_Y))

        box_rect = pygame.Rect(
            text_rect.left - SCOREBOARD_PADDING,
            text_rect.top - SCOREBOARD_PADDING,
            text_rect.width + SCOREBOARD_PADDING * 2,
            text_rect.height + SCOREBOARD_PADDING * 2
        )
        self.box_rect = box_rect

        pygame.draw.rect(window, GRAY, box_rect)
        pygame.draw.rect(window, WHITE, box_rect, SCOREBOARD_BORDER_THICKNESS)
        window.blit(score_text, text_rect)


    