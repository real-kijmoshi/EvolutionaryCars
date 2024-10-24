import pygame
from pygame.math import Vector2
from math import asin
import numpy as np

SPRITE_PATH = "assets/car.png"
CAR_SIZE  = (30, 60)
CAR_ACCELERATION = 5
CAR_MAX_VELOCITY = 10
MAX_ENGINE_POW = 800
CAR_WEIGHT = 200
DRAG_COEFFICIENT = 0.3
GRAVITY = 9.81

COLLISION_MAP = None

next_id = 0



class Car:

    def __init__(self, pos:Vector2 , collisionmap, velocity = Vector2(0,0), angle = 0 , n_sensors = 5 ):
        global next_id

        self.id = next_id

        next_id += 1

        self.pos = pos
        self.velocity= velocity
        self.angle = angle
        self.sprite = pygame.transform.scale(pygame.image.load(SPRITE_PATH), CAR_SIZE)

        self.collisionmap = collisionmap
        self.dead = False

        self.n_sensors  =5
        self.sensors_endpoints = [(pos[0], pos[1])] * n_sensors  # 5 car sensors
        self.sensors_readings = [0] * n_sensors


    def draw(self, win):

        oldRect = self.sprite.get_rect(center=self.pos)

        if not isinstance(self.angle, (int, float)) or not (-360 <= self.angle <= 360):

            self.angle = 0  # Reset angle if it's invalid
        rot_image = pygame.transform.rotate(self.sprite, self.angle)
        rot_rect = rot_image.get_rect(center=oldRect.center)

        win.blit(rot_image, dest=rot_rect)


        for x, y in self.sensors_endpoints:
            pygame.draw.line(win, (0,   0, 255), self.pos, (x, y), 1)


    def update(self, input_vector:Vector2, engine_pow: float,  dt):

        if not self.dead:
            if input_vector != Vector2((0,0)):
                self.velocity += input_vector.normalize() * (engine_pow * MAX_ENGINE_POW - DRAG_COEFFICIENT * GRAVITY*CAR_WEIGHT)* dt


            self.angle= self.velocity.angle_to(Vector2((0,-1)))
            if self.velocity.length() > CAR_MAX_VELOCITY:
            
                self.velocity = self.velocity.normalize() * CAR_MAX_VELOCITY

            self.pos += self.velocity

            alpha = ((self.angle) * np.pi / 180)% np.pi + np.pi
            angle_v = 180 / (self.n_sensors - 1) * np.pi / 180 

            for i in range(self.n_sensors):
                vx = np.cos(angle_v * i - alpha)
                vy = np.sin(angle_v * i - alpha)
                tmp_x, tmp_y = self.pos[0], self.pos[1]
                while self.collisionmap.getpixel((int(tmp_x + vx), int(tmp_y + vy))) == 0:
                    tmp_x += vx
                    tmp_y += vy

                self.sensors_endpoints[i] = (tmp_x, tmp_y)
                self.sensors_readings[i] = np.sqrt(
                    (self.pos[0] - tmp_x) ** 2 + (self.pos[1] - tmp_y) ** 2
                )
            print(self.sensors_readings)
        if self.collisionmap.getpixel(self.pos) != 0:
            self.dead = True

