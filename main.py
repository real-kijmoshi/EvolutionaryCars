import pygame
from PIL import Image
from car import Car, COLLISION_MAP
from pygame.locals import *
from pygame.math import Vector2
import random
import sys
import torch

# Constants
TRACK = "assets/track.png"
COLLISION_MAP = "assets/collisionmap.jpg"
WINDOW_SIZE = (1400, 736)
FRAME_RATE = 120
POPULATION = 30
SURVIVORS = 5
TIME_LIMIT = 10000


current_time = 0
generation = 0

def fitness_fn(x, y):
    #calculate the distance between the car and the finish line
    return ((x - 700)**2 + (y - 50)**2)**0.5


# Main game loop
if __name__ == "__main__":
    pygame.init()
    
    # Initialize cars
    Cars = [
        Car(
            pos=Vector2(350, 680),
            collisionmap=Image.open(COLLISION_MAP).convert('1')
        ) for i in range(POPULATION)
    ]
    
    # Setup pygame
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.image.load(TRACK)
    
    # Main game loop
    while True:
        current_time = (current_time + clock.get_time()) % TIME_LIMIT

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Draw background
        screen.blit(bg, (0, 0))
        
        # Update and draw cars
        dead_count = 0
        for car in Cars:
            car.draw(screen)
            car.update(
                input_vector=Vector2(1, 0.5),
                engine_pow=random.random(),
                dt=clock.get_time()
            )

            if car.dead:
                dead_count += 1
        
        # Check if all cars are dead
        if dead_count == POPULATION:
            generation += 1
            print("-"*20)
            print("population dead")
            print("Generation:", generation)

            # Sort cars by fitness function
            Cars.sort(key=lambda car: fitness_fn(car.pos[0], car.pos[1]), reverse=True)

            # Select survivors
            survivors = Cars[:SURVIVORS]
            print("Survivors:", len(survivors))
            print("Best fitness:", fitness_fn(survivors[0].pos[0], survivors[0].pos[1]))

            # Breed survivors
            new_generation = []
            
            for i in range(POPULATION - SURVIVORS):
                parent1 = random.choice(survivors).brain
                parent2 = random.choice(survivors).brain
                child_brain = parent1.crossover(parent2)
                child = Car(
                    pos=Vector2(350, 680),
                    collisionmap=Image.open(COLLISION_MAP).convert('1')
                )
                child.brain = child_brain

                new_generation.append(child)

                
            # Update cars
            Cars = survivors + new_generation

            for car in Cars:
                car.brain.mutate(1)


            # Reset cars
            for car in Cars:
                car.dead = False
                car.pos = Vector2(350, 680)
                car.velocity = Vector2(0, 0)
                car.angle = 0
                car.sensors_endpoints = [(car.pos[0], car.pos[1])] * car.n_sensors
                car.sensors_readings = [0] * car.n_sensors
            
            print("-"*20)

        # Update display and maintain frame rate
        pygame.display.update()
        clock.tick(FRAME_RATE)