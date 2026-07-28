import math
import pygame
from constants import *

class Paddle:
    def __init__(self, rink, keys, color, half=None):
        #identity
        self.keys = keys
        self.color = color
        self.half = half

        #size/speed
        self.radius = PADDLE_RADIUS
        self.speed = PADDLE_SPEED
        self.dash_speed = PADDLE_DASH_SPEED

        #position//accounting for local mulitplayer
        if half == 'bottom':
            self.paddle_x = rink.x + rink.width // 2
            self.paddle_y = rink.y + rink.height * 3 // 4
        elif half == 'top':
            self.paddle_x = rink.x + rink.width // 2
            self.paddle_y = rink.y + rink.height // 4
        else:
            self.paddle_x = rink.x + rink.width // 4
            self.paddle_y = rink.y + rink.height // 2

        self.prev_x = self.paddle_x
        self.prev_y = self.paddle_y

        #motions
        self.velocity_x = 0
        self.velocity_y = 0

        #input/dash state
        self.prev_keys = pygame.key.get_pressed()
        self.last_press_time = {}
        self.dash_end_time = 0

    def update_paddle(self, rink):
        #following keyboard input
        pressed = pygame.key.get_pressed()
        now = pygame.time.get_ticks() # current time in millisecpnds

        #To handle dash duration
        for key in self.keys.values():
            if pressed[key] and not self.prev_keys[key]:
                if key in self.last_press_time and now - self.last_press_time[key] < PADDLE_DASH_WINDOW: #double tap
                    self.dash_end_time = now + PADDLE_DASH_DURATION
                self.last_press_time[key] = now
        current_speed = self.dash_speed if now < self.dash_end_time else self.speed
        self.prev_keys = pressed

        #user control for pykeys dictionary
        if pressed[self.keys['left']]:
            self.paddle_x -= current_speed
        if pressed[self.keys['right']]:
            self.paddle_x += current_speed
        if pressed[self.keys['up']]:
            self.paddle_y -= current_speed
        if pressed[self.keys['down']]:
            self.paddle_y += current_speed

        #collision checking paddle hitting left wall
        if self.paddle_x - self.radius < rink.left:
            self.paddle_x = rink.left + self.radius

        #right wall
        if self.paddle_x + self.radius > rink.right:
            self.paddle_x = rink.right - self.radius
        
        #top wall
        if self.paddle_y - self.radius < rink.top:
            in_top_goal = rink.top_goal.left <= self.paddle_x <= rink.top_goal.right
            if not in_top_goal:
                self.paddle_y = rink.top + self.radius

        #bottom wall
        if self.paddle_y + self.radius > rink.bottom:
            in_bottom_goal = rink.bottom_goal.left <= self.paddle_x <= rink.bottom_goal.right
            if not in_bottom_goal:
                self.paddle_y = rink.bottom - self.radius

        #goal walls
        self._check_goal_walls(rink)


        # measuring how far the paddle moved this frame = its velocity
        self.velocity_x = self.paddle_x - self.prev_x
        self.velocity_y = self.paddle_y - self.prev_y

        # remembering position for next frame
        self.prev_x = self.paddle_x
        self.prev_y = self.paddle_y


    def _check_goal_walls(self, rink):
        if self.paddle_y < rink.top:
            if self.paddle_x - self.radius < rink.top_goal.left:
                self.paddle_x = rink.top_goal.left + self.radius
            if self.paddle_x + self.radius > rink.top_goal.right:
                self.paddle_x = rink.top_goal.right - self.radius
            if self.paddle_y - self.radius < rink.top_goal.top:
                self.paddle_y = rink.top_goal.top + self.radius

        if self.paddle_y > rink.bottom:
            if self.paddle_x - self.radius < rink.bottom_goal.left:
                self.paddle_x = rink.bottom_goal.left + self.radius
            if self.paddle_x + self.radius > rink.bottom_goal.right:
                self.paddle_x = rink.bottom_goal.right - self.radius
            if self.paddle_y + self.radius > rink.bottom_goal.bottom:
                self.paddle_y = rink.bottom_goal.bottom - self.radius
    
    #still not entirely sure what the underlying math of this is I copy and pasted it from the puck and original paddle code
    def check_paddle_collision(self, other_paddle):
        dx = self.paddle_x - other_paddle.paddle_x      
        dy = self.paddle_y - other_paddle.paddle_y
        distance = math.sqrt(dx**2 + dy **2)

        if distance < self.radius + other_paddle.radius:
            if distance == 0:
                distance = 0.1
            nx = dx / distance
            ny = dy / distance
            overlap = self.radius + other_paddle.radius - distance
            self.paddle_x += nx * overlap / 2           
            self.paddle_y += ny * overlap / 2
            other_paddle.paddle_x -=nx * overlap / 2
            other_paddle.paddle_y -=ny * overlap/ 2
        
    def reset_paddle(self, rink):
        if self.half == 'bottom':
            self.paddle_x = rink.x + rink.width // 2
            self.paddle_y = rink.y + rink.height * 3 // 4
        elif self.half == 'top':
            self.paddle_x = rink.x + rink.width // 2
            self.paddle_y = rink.y + rink.height // 4
        self.velocity_x = 0
        self.velocity_y = 0


    def draw_paddle(self, window):
        pygame.draw.circle(window, self.color, (self.paddle_x, self.paddle_y), self.radius)


