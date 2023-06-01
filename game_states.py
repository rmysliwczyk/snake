import pygame
from constants import *
from state_machine import StateMachine
from game_objects import SnakePart, Collectible, Text


class BaseState:
    def __init__(self):
        ...
    
    def update(self, clock):
        ...

    def draw(self):
        ...


class TitleState(BaseState):
    def __init__(self):
        super().__init__()
        self.title_text = Text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, "SNAKE")
        self.time_passed = 0

    def update(self, clock):
        super().update(clock)
        self.time_passed += clock.get_time()
        if self.time_passed > 10:
            try:
                self.title_text.change_alpha(-2)
            except ValueError:
                StateMachine.change_current(PlayState())
            self.time_passed = 0

    def draw(self):
        super().draw()
        self.title_text.draw()


class PlayState(BaseState):
    def __init__(self):
        self.play_area = pygame.Surface((MAP_W * TILE_SIZE, MAP_H * TILE_SIZE))
        self.snake = SnakePart((MAP_W-1)/2 * TILE_SIZE, (MAP_H-1)/2  * TILE_SIZE, head=True)
        self.move_threshold = 0
        self.game_over = False
        self.current_collectible = None
        self.direction_queue = []
        self.overlay_text = None
        self.score = 0

    def update(self, clock):
        keys_pressed = pygame.key.get_pressed()
        if len(self.direction_queue) < 3:
            if keys_pressed[pygame.K_UP]:
                if "u" not in self.direction_queue:
                    self.direction_queue.append("u")
            elif keys_pressed[pygame.K_DOWN]:
                if "d" not in self.direction_queue:
                    self.direction_queue.append("d")
            elif keys_pressed[pygame.K_LEFT]:
                if "l" not in self.direction_queue:
                    self.direction_queue.append("l")
            elif keys_pressed[pygame.K_RIGHT]:
                if "r" not in self.direction_queue:
                    self.direction_queue.append("r")

        self.move_threshold += clock.get_time() * self.snake.speed
        if self.move_threshold >= 1000 and self.game_over is False:
            self.move_threshold = 0
            if self.current_collectible:
                self.current_collectible.lifetime -= 1
                if self.current_collectible.lifetime < 10:
                    self.current_collectible.color = "blue"
                elif self.current_collectible.lifetime <= 0:
                    self.current_collectible = None

                if self.snake.collides(self.current_collectible):
                    self.snake.spawn_new_part()
                    self.score += 10
                    self.current_collectible = None
            else:
                while True:
                    self.current_collectible = Collectible.spawn_collectible()
                    collectible_spawned = True
                    snake_part = self.snake
                    while snake_part:
                        if self.current_collectible.collides(snake_part):
                            collectible_spawned = False
                        snake_part = snake_part.attaching
                    if collectible_spawned:
                        break

            if len(self.direction_queue) > 0:
                self.snake.change_direction(self.direction_queue.pop(0))
            self.snake.update()
            if self.snake.check_collision_with_self():
                self.game_over = True

        if self.game_over:
            self.overlay_text = Text(
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                150, "GAME OVER", "red"
                )
        else:
            self.overlay_text = Text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - (TILE_SIZE * MAP_H)/2 - 15, 50, f"SCORE: {self.score}")
    def draw(self):
        
        self.play_area.fill("white")

        if self.current_collectible:
            self.current_collectible.draw(self.play_area)

        current_snake_part = self.snake
        while True:
            current_snake_part.draw(self.play_area)
            current_snake_part = current_snake_part.attaching
            if current_snake_part is None:
                break

        pygame.display.get_surface().blit(self.play_area, (SCREEN_WIDTH/2 - (MAP_W * TILE_SIZE / 2), SCREEN_HEIGHT/2 - (MAP_H * TILE_SIZE / 2)))

        if self.overlay_text:
            self.overlay_text.draw()

