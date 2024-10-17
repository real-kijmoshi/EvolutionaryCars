import pygame
from PIL import Image
from car import Car, COLLISION_MAP
from pygame.locals import *
from pygame.math import Vector2
import random
import sys

TRACK = "assets/track.png"
COLLISION_MAP = "assets/collisionmap.jpg"

WINDOW_SIZE = (1400, 736)
FRAME_RATE = 120

if __name__ == "__main__":
    print("halo")
    pygame.init()

    car = Car((350, 680), collisionmap = Image.open(COLLISION_MAP).convert('1'))

    clock = pygame.time.Clock()


    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg= pygame.image.load(TRACK)
    

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


        screen.blit(bg, Vector2(0,0))
        car.draw(screen)

        car.update(Vector2(1, 0.1), random.random() ,clock.get_time())

        pygame.display.update()

        clock.tick(FRAME_RATE)