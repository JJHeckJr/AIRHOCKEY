import pygame
from constants import *
from paddle import Paddle
from puck import Puck
from game_base_class import GameBaseMode
from timer import Timer

class LocalGame(GameBaseMode):
    def __init__(self, window):
        super().__init__(window)
        self.paddle1 = Paddle(self.rink, P1_KEYS, RED, half='bottom')
        self.paddle2 = Paddle(self.rink, P2_KEYS, GREEN, half='top')
        self.countdown_timer = 0
        self.timer = Timer()

    def set_vs_cpu(self, vs_cpu):
        self.paddle2.is_cpu = vs_cpu

    def handle_ui_events(self, event):
        next_state = super().handle_ui_events(event)
        if next_state is not None:
            return next_state
        if self.timer.time_up and self.rematch_button.is_clicked(event):
            self.reset_match()
        return None

    def update(self):
        if self.paused_game:
            return
        if self.timer.time_up:
            return
        if self.countdown_timer > 0:
            self.countdown_timer -= 1
            return
        self.timer.update_score()
        self.puck.move()
        self.puck.check_rink_walls(self.rink)
        self.puck.check_paddle_collision(self.paddle1)
        self.puck.check_paddle_collision(self.paddle2)
        self.paddle1.update_paddle(self.rink)
        self.paddle2.update_paddle(self.rink, self.puck)
        self.paddle1.check_paddle_collision(self.paddle2)
        self.paddle1._check_center_line(self.rink)
        self.paddle2._check_center_line(self.rink)
        self._update_flash()

    def draw(self, window):
        self.rink.draw_rink(window)
        if self.flash_timer > 0:
            self._draw_flash(window)
        self.puck.draw_puck(window)
        self.paddle1.draw_paddle(window)
        self.paddle2.draw_paddle(window)
        if self.countdown_timer > 0:
            count = (self.countdown_timer // 60) + 1
            font = pygame.font.Font(None, 200)
            text = font.render(str(count), True, WHITE)
            w, h = window.get_width(), window.get_height()
            window.blit(text, text.get_rect(center=(w // 2, h // 2)))
        self.scoreboard.draw_scoreboard(window, self.rink)
        self.timer.draw_timer(window, self.scoreboard.box_rect)
        self._draw_pause_overlay(window)
        self._draw_winner_overlay(window)

    def _on_goal_reset(self):
        self.puck.reset(self.rink, self.flash_goal)
        self.paddle1.reset_paddle(self.rink)
        self.paddle2.reset_paddle(self.rink)
        self.countdown_timer = 180

    def reset_match(self):
        self.scoreboard.top_score = 0
        self.scoreboard.bottom_score = 0
        self.timer.reset()
        self.puck = Puck(self.rink)
        self.paddle1.reset_paddle(self.rink)
        self.paddle2.reset_paddle(self.rink)
        self.flash_goal = None
        self.flash_timer = 0
        self.countdown_timer = 180