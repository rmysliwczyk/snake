import pygame
from enum import Enum
from game_states import TitleState, PlayState


class GameStates(Enum):
    title_state = TitleState()
    play_state = PlayState()


class StateMachine:
    current_state = None
    @classmethod
    def change_current(cls, state=title_state):
        cls.current_state = state

    @classmethod
    def update_current(cls, clock):
        cls.current_state.update(clock)
    
    @classmethod
    def draw_current(cls):
        cls.current_state.draw()


