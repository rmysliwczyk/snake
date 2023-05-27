import pygame
from constants import *
from BaseState import BaseState
from StateMachine import StateMachine
from Snake import SnakePart
from Text import Text

class PlayState(BaseState):
    def __init__(self):
        self.snake = SnakePart(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, head=True)
        self.move_threshold = 0
    
    def update(self, clock):
        # For debuging purposes:
        spawn_new_part = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] == True:
            if self.snake.direction != "d":
                self.snake.direction = "u"
        elif keys_pressed[pygame.K_DOWN] == True:
            if self.snake.direction != "u":
                self.snake.direction = "d"
        elif keys_pressed[pygame.K_LEFT] == True:
            if self.snake.direction != "r":
                self.snake.direction = "l"
        elif keys_pressed[pygame.K_RIGHT] == True:
            if self.snake.direction != "l":
                self.snake.direction = "r"
        if keys_pressed[pygame.K_RETURN] == True:
            spawn_new_part = True


        self.move_threshold += clock.get_time() * self.snake.speed
        if self.move_threshold >= 1000:
            
            # For debuging purposes
            if spawn_new_part == True:
                self.snake.spawn_new_part()

            self.snake.update()
            self.move_threshold = 0


    def draw(self):
        current_snake_part = self.snake
        while True:
            current_snake_part.draw()
            current_snake_part = current_snake_part.attaching
            if current_snake_part == None:
                break