import pygame
from pygame.math import Vector2
from math import asin

SPRITE_PATH = "assets/car.png"
CAR_SIZE  = (30, 60)
CAR_ACCELERATION = 5
CAR_MAX_VELOCITY = 10
MAX_ENGINE_POW = 800
CAR_WEIGHT = 200
DRAG_COEFFICIENT = 0.3
GRAVITY = 9.81


next_id = 0



class Car:

    def __init__(self, pos:Vector2 ,velocity = Vector2(0,0), angle = 0  ):
        global next_id

        self.id = next_id

        next_id += 1

        self.pos = pos
        self.velocity= velocity
        self.angle = angle
        self.sprite = pygame.transform.scale(pygame.image.load(SPRITE_PATH), CAR_SIZE)


    def draw(self, win):

        oldRect = self.sprite.get_rect(center=self.pos)

        print(self.angle)
        if not isinstance(self.angle, (int, float)) or not (-360 <= self.angle <= 360):
            print(self.angle)
            self.angle = 0  # Reset angle if it's invalid
        rot_image = pygame.transform.rotate(self.sprite, self.angle)
        rot_rect = rot_image.get_rect(center=oldRect.center)

        win.blit(rot_image, dest=rot_rect)


    def update(self, input_vector:Vector2, engine_pow: float,  dt):
  
        self.velocity += input_vector.normalize() * (engine_pow * MAX_ENGINE_POW - DRAG_COEFFICIENT * GRAVITY*CAR_WEIGHT)* dt

        try: 
            self.angle = asin(self.velocity.y/self.velocity.x) / 3.14 * 180 / 2
        except:
            self.angle= 0
        if self.velocity.length() > CAR_MAX_VELOCITY:
        
            self.velocity = self.velocity.normalize() * CAR_MAX_VELOCITY

        self.pos += self.velocity
