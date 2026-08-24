from constants import *
from paddle import Paddle
from puck import Puck
from game_base_class import GameBaseMode

class Practice(GameBaseMode):
    def __init__(self, window):
        super().__init__(window)
        self.paddle = Paddle(self.rink, P1_KEYS, RED)

    def reset_match(self):
        super().reset_match()
        self.paddle.reset_paddle(self.rink)
        self.puck = Puck(self.rink)

    def update(self):
        if self.paused_game:
            return
        self.puck.move()
        self.puck.check_rink_walls(self.rink)
        self.puck.check_paddle_collision(self.paddle)
        self.paddle.update_paddle(self.rink)
        self._update_flash()

    def draw(self, window):
        self.rink.draw_rink(window)
        if self.flash_timer > 0:
            self._draw_flash(window)
        self.puck.draw_puck(window)
        self.paddle.draw_paddle(window)
        self.scoreboard.draw_scoreboard(window, self.rink)
        self._draw_pause_overlay(window)

    