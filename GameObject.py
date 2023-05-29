import pygame


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
