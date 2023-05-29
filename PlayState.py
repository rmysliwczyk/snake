import pygame
from constants import *
from BaseState import BaseState
from StateMachine import StateMachine
from Collectible import Collectible
from Snake import SnakePart
from Text import Text

class PlayState(BaseState):
    def __init__(self):
        self.snake = SnakePart(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, head=True)
        self.move_threshold = 0
        self.game_over = False
        self.current_collectible = None
        self.direction_queue = []
        self.overlay_text = None
    
    def update(self, clock):

        keys_pressed = pygame.key.get_pressed()
        if len(self.direction_queue) < 3:
            if keys_pressed[pygame.K_UP] == True:
                if "u" not in self.direction_queue:
                    self.direction_queue.append("u")
            elif keys_pressed[pygame.K_DOWN] == True:
                if "d" not in self.direction_queue:
                    self.direction_queue.append("d")
            elif keys_pressed[pygame.K_LEFT] == True:
                if "l" not in self.direction_queue:
                    self.direction_queue.append("l")
            elif keys_pressed[pygame.K_RIGHT] == True:
                if "r" not in self.direction_queue:
                    self.direction_queue.append("r")


        self.move_threshold += clock.get_time() * self.snake.speed
        if self.move_threshold >= 1000 and self.game_over == False:
            self.move_threshold = 0
            if self.current_collectible:
                self.current_collectible.lifetime -= 1
                if self.current_collectible.lifetime < 10:
                    self.current_collectible.color = "blue"
                elif self.current_collectible.lifetime <= 0:
                    self.current_collectible = None  

                if self.snake.collides(self.current_collectible):
                    self.snake.spawn_new_part()
                    self.current_collectible = None
            else:
                while True:
                    self.current_collectible = Collectible.spawn_collectible()
                    collectible_spawned = True
                    current_snake_part = self.snake
                    while current_snake_part:
                        if self.current_collectible.collides(current_snake_part):
                            collectible_spawned = False
                        current_snake_part = current_snake_part.attaching
                    if collectible_spawned == True:
                        break
    
            if len(self.direction_queue) > 0:
                self.snake.change_direction(self.direction_queue.pop(0))
                print(self.snake.direction)
            self.snake.update()
            if self.snake.check_collision_with_self():
                self.game_over = True


        if self.game_over == True:
            self.overlay_text = Text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 150, "GAME OVER", "red")


    def draw(self):
        if self.current_collectible:
            self.current_collectible.draw()

        current_snake_part = self.snake
        while True:
            current_snake_part.draw()
            current_snake_part = current_snake_part.attaching
            if current_snake_part == None:
                break

        if self.overlay_text:
            self.overlay_text.draw()