import pygame
from constants import *

class Rink:

    #Function to draw the rink itself
    def __init__(self, window):
        w = window.get_width()
        h = window.get_height()
        self.width = int(w * RINK_WIDTH)
        self.height = int(h * RINK_HEIGHT)
        self.x = w // 2 - self.width // 2
        self.y = h // 2 - self.height // 2

        #edge names for collisoin/clamp to read naturally
        self.left = self.x
        self.right = self.x + self.width
        self.top = self.y
        self.bottom = self.y + self.height

        #setting our goal width and heigth
        goal_width = int(w * GOAL_WIDTH)
        goal_height = int(h * GOAL_HEIGHT)
        goal_center_x = self.x + self.width // 2 - goal_width // 2

        #creating objects for goals
        self.top_goal = pygame.Rect(goal_center_x, self.y - goal_height, goal_width, goal_height)
        self.bottom_goal = pygame.Rect(goal_center_x, self.y + self.height, goal_width, goal_height)

    def draw_rink(self, window):
        w = window.get_width()
        h = window.get_height()

        #drawing rink
        goal_left = self.top_goal.left
        goal_right = self.top_goal.right

        #left and right wall drawn
        pygame.draw.line(window, WHITE, (self.x, self.y), (self.x, self.y + self.height), RINK_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), RINK_BORDER_THICKNESS)

        #top wall (two segments with gap for goal)
        pygame.draw.line(window, WHITE, (self.x, self.y), (goal_left, self.y), RINK_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, (goal_right, self.y), (self.x + self.width, self.y), RINK_BORDER_THICKNESS)

        #bottom wall (two segments with gap for goal)
        pygame.draw.line(window, WHITE, (self.x, self.y + self.height), (goal_left, self.y + self.height), RINK_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, (goal_right, self.y + self.height), (self.x + self.width, self.y + self.height), RINK_BORDER_THICKNESS)

        
        #center line
        # tuples grab starting and edning position of line
        pygame.draw.line(window, WHITE, (self.x, h // 2), (self.x + self.width, h // 2), RINK_LINE_THICKNESS)

        #top goal drawn
        pygame.draw.line(window, WHITE, self.top_goal.topleft, self.top_goal.bottomleft, GOAL_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, self.top_goal.topleft, self.top_goal.topright, GOAL_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, self.top_goal.topright, self.top_goal.bottomright, GOAL_BORDER_THICKNESS)

        #bottom goal draw
        pygame.draw.line(window, WHITE, self.bottom_goal.bottomleft, self.bottom_goal.topleft, GOAL_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, self.bottom_goal.bottomleft, self.bottom_goal.bottomright, GOAL_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, self.bottom_goal.bottomright, self.bottom_goal.topright, GOAL_BORDER_THICKNESS)

        #goal lines(shows where puck enters goal)
        pygame.draw.line(window, WHITE, (goal_left, self.y), (goal_right, self.y), GOAL_BORDER_THICKNESS)
        pygame.draw.line(window, WHITE, (goal_left, self.y + self.height), (goal_right, self.y + self.height), GOAL_BORDER_THICKNESS)





        



