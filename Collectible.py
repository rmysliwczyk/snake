import pygame
import random
from constants import *
from GameObject import GameObject

class Collectible(GameObject):
    def __init__(self, x, y, w=TILE_WIDTH, h=TILE_HEIGHT, color=DEF_COLLECTIBLE_COLOR, lifetime=COLLECTIBLE_LIFETIME):
        super().__init__(x, y, w, h)
        self.color = color
        self.lifetime = lifetime

    @classmethod
    def spawn_collectible(cls):
        """
        Spawn new collectible in any x and y randomly
        """
        return Collectible((random.randint(1, (SCREEN_WIDTH/TILE_WIDTH) - 1) * TILE_WIDTH), (random.randint(1, SCREEN_HEIGHT/TILE_HEIGHT) - 1) * TILE_HEIGHT)

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, (self.x, self.y, self.w , self.h))