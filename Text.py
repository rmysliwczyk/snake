import pygame
from GameObject import GameObject


class Text(GameObject):
    def __init__(self, center_x, center_y, size, text_string, color="black"):
        self.alpha = 255
        self.text_string = text_string
        self.pg_text_obj = pygame.font.Font(size=size)
        size_x, size_y = self.pg_text_obj.size(text_string)
        center_x = center_x - size_x/2
        center_y = center_y - size_y/2
        super().__init__(center_x, center_y)
        self.pg_text_obj = self.pg_text_obj.render(text_string, True, color)

    def change_alpha(self, n):
        if n < 0 and self.pg_text_obj.get_alpha() <= 0:
            raise ValueError("Can't make alpha less than 0")
        elif n > 0 and self.pg_text_obj.get_alpha() >= 255:
            raise ValueError("Can't make alpha more than 255")
        else:
            self.alpha = self.pg_text_obj.get_alpha() + n
            self.pg_text_obj.set_alpha(self.alpha)

    def draw(self):
        pygame.display.get_surface().blit(
            self.pg_text_obj,
            (self.x,
             self.y,)
        )
