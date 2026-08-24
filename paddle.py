import math
import pygame
from constants import *

class Paddle:
    def __init__(self, rink, keys, color, half=None, is_cpu=False):
        #identity
        self.keys = keys
        self.color = color
        self.half = half
        self.is_cpu = is_cpu
        self.reaction_delay_frames = CPU_REACTION_DELAY_FRAMES
        self.puck_history = []

        #size/speed
        self.radius = PADDLE_RADIUS
        self.speed = PADDLE_SPEED
        self.dash_speed = PADDLE_DASH_SPEED
        self.cpu_speed = CPU_PADDLE_SPEED

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

        #home spot the cpu returns to
        self.home_x = self.paddle_x
        self.home_y = self.paddle_y

        self.prev_x = self.paddle_x
        self.prev_y = self.paddle_y

        #motions
        self.velocity_x = 0
        self.velocity_y = 0

        #input/dash state
        self.prev_keys = pygame.key.get_pressed()
        self.last_press_time = {}
        self.dash_end_time = 0

    def update_paddle(self, rink, puck=None):
        if self.is_cpu:
            self._move_cpu(rink, puck)
        else:
            #following keyboard input
            pressed = pygame.key.get_pressed() #pygame function grabbing the current state of a key being pressed
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

        #Center-line restriction
        self._check_center_line(rink)

        #goal walls
        self._check_goal_walls(rink)


        # measuring how far the paddle moved this frame = its velocity
        self.velocity_x = self.paddle_x - self.prev_x
        self.velocity_y = self.paddle_y - self.prev_y

        # remembering position for next frame
        self.prev_x = self.paddle_x
        self.prev_y = self.paddle_y

    def _percieved_puck_position(self, puck):
        self.puck_history.append((puck.puck_x, puck.puck_y))
        if len(self.puck_history) > self.reaction_delay_frames:
            return self.puck_history.pop(0)
        return self.home_x, self.home_y

    def _apply_deadzone(self, target_x, target_y): 
        if abs(target_x - self.paddle_x) < CPU_TRACKING_DEADZONE:
            target_x = self.paddle_x
        if abs(target_y -self.paddle_y) < CPU_TRACKING_DEADZONE:
            target_y = self.paddle_y
        return target_x, target_y

    def _predicted_puck_position(self, base_x, base_y, puck):
        predicted_x = base_x + puck.velocity_x * CPU_PREDICTION_FRAMES
        predicted_y = base_y + puck.velocity_y * CPU_PREDICTION_FRAMES
        return predicted_x, predicted_y
    
    def _urgency_speed(self, rink, puck):
        own_goal = rink.top_goal if self.half == 'top' else rink.bottom_goal
        goal_distance = math.hypot(puck.puck_x - own_goal.centerx, puck.puck_y - own_goal.centery)
        if goal_distance >= CPU_URGENCY_RANGE:
            return self.cpu_speed
        urgency = 1 - (goal_distance / CPU_URGENCY_RANGE)
        return self.cpu_speed + urgency * (CPU_MAX_URGENCY_SPEED - self.cpu_speed)

    def _move_cpu(self, rink, puck):
        if puck is None:
            target_x, target_y = self.home_x, self.home_y
            speed = self.cpu_speed
        else:
            mid_y = rink.y + rink.height // 2
            on_our_half = self._puck_on_our_half(puck, mid_y)
            distance_to_puck = math.hypot(puck.puck_x - self.paddle_x, puck.puck_y - self.paddle_y)

            if not on_our_half:
                target_x, target_y = self.home_x, self.home_y
                speed = self.cpu_speed
            elif distance_to_puck < CPU_AIM_RANGE:
                target_x, target_y = self._aim_at_goal(rink, puck)
                speed = self._urgency_speed(rink, puck)
            else:
                perceived_x, perceived_y = self._percieved_puck_position(puck)
                predicted_x, predicted_y = self._predicted_puck_position(perceived_x, perceived_y, puck)
                target_x, target_y = self._apply_deadzone(predicted_x, predicted_y)
                speed = self.cpu_speed

        #cacluating distance between puck and paddle
        dx = target_x - self.paddle_x
        dy = target_y - self.paddle_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        move = min(speed, distance)
        self.paddle_x += dx / distance * move
        self.paddle_y += dy / distance * move

    def _puck_on_our_half(self, puck, mid_y):
        if self.half == 'top':
            return puck.puck_y < mid_y
        return puck.puck_y > mid_y

    def _aim_at_goal(self, rink, puck):
        goal = rink.bottom_goal if self.half =='top' else rink.top_goal
        goal_x, goal_y = goal.centerx, goal.centery

        #vector pointing from the goal through the puck, extended a bit
        away_x = puck.puck_x - goal_x
        away_y = puck.puck_y - goal_y
        away_distance = math.hypot(away_x, away_y)
        if away_distance == 0:
            return puck.puck_x, puck.puck_y

        approach_gap = self.radius + puck.radius
        target_x = puck.puck_x + (away_x / away_distance) * approach_gap
        target_y = puck.puck_y + (away_y / away_distance) * approach_gap
        return target_x, target_y
    
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

    def _check_center_line(self, rink):
        mid_y = rink.y + rink.height // 2
        if self.half == 'top' and self.paddle_y + self.radius > mid_y:
            self.paddle_y = mid_y - self.radius
        elif self.half == 'bottom' and self.paddle_y - self.radius < mid_y:
            self.paddle_y = mid_y + self.radius
    
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


