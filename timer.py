import pygame
from constants import *

class Timer:
    def __init__(self, duration_seconds=TIMER_DURATION_SECONDS):
        self.duration_frames = duration_seconds * FPS
        self.frames_remaining = self.duration_frames
        self.time_up = False

    def update_score(self):
        if self.frames_remaining > 0:
            self.frames_remaining -= 1
            if self.frames_remaining == 0:
                self.time_up = True

    def reset(self):
        self.frames_remaining = self.duration_frames
        self.time_up = False

    def get_time_string(self):
        total_seconds = self.frames_remaining // FPS
        minutes, seconds = divmod(total_seconds, 60) #returns quotient and remainder of dividing a by b, as a tuple shortcuts for a// b, a % b.
        return f"{minutes}:{seconds:02d}"

    def draw_timer(self, window, anchor_rect):
        font = pygame.font.Font(None, SCOREBOARD_FONT_SIZE)
        timer_text = font.render(self.get_time_string(), True, WHITE)
        text_rect = timer_text.get_rect(midtop=(anchor_rect.centerx, anchor_rect.bottom + TIMER_GAP_Y))

        box_rect = pygame.Rect( #visual padding
            text_rect.left - SCOREBOARD_PADDING,
            text_rect.top - SCOREBOARD_PADDING,
            text_rect.width + SCOREBOARD_PADDING * 2,
            text_rect.height + SCOREBOARD_PADDING * 2
        )
        pygame.draw.rect(window, GRAY, box_rect)
        pygame.draw.rect(window, WHITE, box_rect, SCOREBOARD_BORDER_THICKNESS)
        window.blit(timer_text, text_rect)



