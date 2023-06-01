import pygame
import random
from constants import *

class GameObject:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def collides(self, other):
        """
        Check box collision

        :param self: This object
        :type self: GameObject
        :return: GameObject or None
        :rtype: GameObject or None
        """

        if self.x + self.w > other.x and self.x < other.x + other.w:
            if self.y + self.h > other.y and self.y < other.y + other.h:
                return other
            else:
                return None
        else:
            return None


class Text(GameObject):
    def __init__(self, center_x, center_y, size, text_string, color="black"):
        self.alpha = 255
        self.text_string = text_string
        self.pg_text_obj = pygame.font.Font(None, size=size)
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


class SnakePart(GameObject):
    def __init__(
                self, x, y, head=False,
                w=TILE_SIZE, h=TILE_SIZE,
                attached_to=None, speed=3
            ):
        super().__init__(x, y, w, h)
        self.color = "red" if head else "black"

        # Position before part was moved
        self.prev_x = x
        self.prev_y = y

        # Head specific
        self.head = head
        self.speed = speed
        self.direction = ""
        self.speed = speed

        # Snake is a doubly linked list
        if head:
            self.attached_to = None
        else:
            self.attached_to = attached_to
        self.attaching = None

    def update(self):
        if self.head:
            self.prev_x = self.x
            self.prev_y = self.y
            match self.direction:
                case "u":
                    self.y = self.y - self.h
                    if self.y < 0:
                        self.y = SCREEN_HEIGHT - self.h
                case "d":
                    self.y = self.y + self.h
                    if self.y >= SCREEN_HEIGHT:
                        self.y = 0
                case "l":
                    self.x = self.x - self.w
                    if self.x < 0:
                        self.x = SCREEN_WIDTH - self.w
                case "r":
                    self.x = self.x + self.w
                    if self.x >= SCREEN_WIDTH:
                        self.x = 0
                case _:
                    ...
        else:
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = self.attached_to.prev_x
            self.y = self.attached_to.prev_y
        if self.attaching:
            try:
                self.attaching.update()
            except RecursionError:
                raise RecursionError("Snake too long")

    def spawn_new_part(self):
        current_part = self
        while current_part:
            if current_part.attaching is None:
                current_part.attaching = (
                    SnakePart(
                        current_part.x, current_part.y,
                        attached_to=current_part
                        )
                    )

                # Return when spawning complete to break the loop
                return
            else:
                current_part = current_part.attaching

    def check_collision_with_self(self):
        current_part = self.attaching
        while current_part:
            if type(self.collides(current_part)) == SnakePart:
                self.collides(current_part).color = "yellow"
                return True

            current_part = current_part.attaching

        return False

    def change_direction(self, direction):
        if direction == "u":
            if self.direction != "d":
                self.direction = "u"
        elif direction == "d":
            if self.direction != "u":
                self.direction = "d"
        elif direction == "l":
            if self.direction != "r":
                self.direction = "l"
        elif direction == "r":
            if self.direction != "l":
                self.direction = "r"

    def draw(self):
        pygame.draw.rect(
            pygame.display.get_surface(), self.color,
            (self.x, self.y, self.w, self.h)
            )


class Collectible(GameObject):
    def __init__(
            self, x, y, w=TILE_SIZE, h=TILE_SIZE,
            color=DEF_COLLECTIBLE_COLOR,
            lifetime=COLLECTIBLE_LIFETIME
        ):
        super().__init__(x, y, w, h)
        self.color = color
        self.lifetime = lifetime

    @classmethod
    def spawn_collectible(cls):
        """
        Spawn new collectible in any x and y randomly
        """
        return Collectible((random.randint(1, (SCREEN_WIDTH/TILE_SIZE) - 1) * TILE_SIZE), (random.randint(1, SCREEN_HEIGHT/TILE_SIZE) - 1) * TILE_SIZE)

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, (self.x, self.y, self.w , self.h))
