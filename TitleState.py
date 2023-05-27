import pygame
from constants import *
from BaseState import BaseState
from StateMachine import StateMachine
from PlayState import PlayState
from Text import Text

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
        screen = pygame.display.get_surface()

        self.title_text.draw()