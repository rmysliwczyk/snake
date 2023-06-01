import pygame
from constants import *
from state_machine import StateMachine
from game_states import TitleState


def main():
    if pygame.init() != (5, 0):
        raise pygame.error("Not all modules were loaded")

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SNAKE")

    StateMachine().change_current(TitleState())

    clock = pygame.time.Clock()

    update(clock)


def update(clock):
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        StateMachine().update_current(clock)
        draw()
        clock.tick()


def draw():
    pygame.display.get_surface().fill("gray")

    StateMachine().draw_current()
    pygame.display.flip()

if __name__ == "__main__":
    main()
