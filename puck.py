import pygame
import math
from constants import *


class Puck:

    def __init__(self, rink):
        self.puck_x = rink.x + rink.width // 2
        self.puck_y = rink.y + rink.height // 2
        self.radius  = PUCK_RADIUS
        self.velocity_x = PUCK_SPEED
        self.velocity_y = PUCK_SPEED

    #Drawing our puck
    def draw_puck(self, window):
        pygame.draw.circle(window, BLUE, (self.puck_x, self.puck_y), self.radius)

    #creating movement for it
    def move(self):
        self.velocity_x *= PUCK_FRICTION
        self.velocity_y *= PUCK_FRICTION
        self.puck_x += self.velocity_x
        self.puck_y += self.velocity_y

        constant_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if 0 < constant_speed < PUCK_MIN_SPEED:
            self.velocity_x = (self.velocity_x / constant_speed) * PUCK_MIN_SPEED
            self.velocity_y = (self.velocity_y / constant_speed) * PUCK_MIN_SPEED

    def _check_goal_walls(self, goal, back_wall_is_top):
        if back_wall_is_top:
            if self.puck_y - self.radius <= goal.top:
                self.puck_y = goal.top + self.radius
                self.velocity_y *= -1
        else:
                if self.puck_y + self.radius >= goal.bottom:
                    self.puck_y = goal.bottom - self.radius
                    self.velocity_y *= -1
        if self.puck_x - self.radius <= goal.left:
                self.puck_x = goal.left + self.radius
                self.velocity_x *= -1
        elif self.puck_x + self.radius >= goal.right:
                self.puck_x = goal.right - self.radius
                self.velocity_x *= -1

    def check_rink_walls(self, rink):
        left_wall = rink.x
        right_wall = rink.x + rink.width
        top_wall = rink.y
        bottom_wall = rink.y + rink.height

        # left wall  
        if self.puck_x - self.radius <= left_wall:
            self.puck_x = left_wall + self.radius
            self.velocity_x *= -1

        # right wall
        elif self.puck_x + self.radius >= right_wall:
            self.puck_x = right_wall - self.radius
            self.velocity_x *= -1

        # top wall (skip bounce if puck is in goal opening)
        if self.puck_y - self.radius <= top_wall:
            in_top_goal = rink.top_goal.left <= self.puck_x <= rink.top_goal.right
            if not in_top_goal:
                self.puck_y = top_wall + self.radius
                self.velocity_y *= -1
        # bottom wall
        elif self.puck_y + self.radius >= bottom_wall:
            in_bottom_goal = rink.bottom_goal.left <= self.puck_x <= rink.bottom_goal.right
            if not in_bottom_goal:
                self.puck_y = bottom_wall - self.radius
                self.velocity_y *= -1

        if self.puck_y < rink.top:
             self._check_goal_walls(rink.top_goal, back_wall_is_top=True)
        elif self.puck_y > rink.bottom:
             self._check_goal_walls(rink.bottom_goal, back_wall_is_top=False)

    def check_paddle_collision(self, paddle):
        #checking distance between padddle and puck
        dx = self.puck_x - paddle.paddle_x
        dy = self.puck_y - paddle.paddle_y

        distance = math.sqrt(dx**2 + dy ** 2)

        if distance <= self.radius + paddle.radius:
            if distance == 0: #avoid game crash
                distance = 0.1

        # --- bounce math (revisit later) -----
        # sends puck away at current speed
        # nudges so it doesnt get stuck
            nx = dx / distance
            ny = dy / distance
            incoming_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            self.velocity_x = nx * incoming_speed
            self.velocity_y = ny * incoming_speed

            #adding paddle's own motion - hard swing hits harder
            self.velocity_x += paddle.velocity_x
            self.velocity_y += paddle.velocity_y

            #capping speed so the puck can't tunnel through
            final_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if final_speed > PUCK_MAX_SPEED:
                self.velocity_x = (self.velocity_x / final_speed) * PUCK_MAX_SPEED
                self.velocity_y = (self.velocity_y / final_speed) * PUCK_MAX_SPEED

            #push the puck out so it doesnt stick
            overlap = self.radius + paddle.radius - distance
            self.puck_x += nx * overlap
            self.puck_y += ny * overlap
    
    #checking for scored goal for practice to flash
    def check_scored_goal(self, rink):
         in_top_goal = rink.top_goal.left <= self.puck_x <= rink.top_goal.right
         in_bottom_goal = rink.bottom_goal.left <= self.puck_x <= rink.bottom_goal.right

         if self.puck_y - self.radius <= rink.top and in_top_goal:
              return 'top'
         if self.puck_y + self.radius >= rink.bottom and in_bottom_goal:
              return 'bottom'
         return None

    def reset(self, rink, goal):
        self.velocity_x = PUCK_SPEED
        self.velocity_y = PUCK_SPEED
        if goal == 'top':
            self.puck_x = rink.x + rink.width // 2
            self.puck_y = rink.top + rink.height // 4
        elif goal == 'bottom':
             self.puck_x = rink.x + rink.width // 2
             self.puck_y = rink.top + rink.height * 3 // 4
        




        




