import pygame
from constants import *
from GameObject import GameObject

class SnakePart(GameObject):
    def __init__(self, x, y, head=False, w=25, h=25, attached_to=None, speed=5):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.color = "red" if head else "black"
        
        # Last position, of this part. Used for sequential movement of all parts
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
            if self.head == True:
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
            if current_part.attaching == None:
                current_part.attaching = (SnakePart(current_part.x, current_part.y, attached_to=current_part))

                # Return when spawning complete to break the loop
                return
            else:
                current_part = current_part.attaching

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, (self.x, self.y, self.w, self.h))
