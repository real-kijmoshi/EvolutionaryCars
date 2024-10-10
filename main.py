import pygame
from PIL import Image
from car import Car
from pygame.locals import *
from pygame.math import Vector2
import random
import sys

WINDOW_SIZE = (1400, 736)
FRAME_RATE = 120

if __name__ == "__main__":
    print("halo")
    pygame.init()

    car = Car((700, 350))

    clock = pygame.time.Clock()


    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg= pygame.image.load("assets/track.png")

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


        screen.blit(bg, Vector2(0,0))
        car.draw(screen)

        car.update(Vector2(0.5, 0.5), random.random() ,clock.get_time())

        pygame.display.update()

        clock.tick(FRAME_RATE)