import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_POINTS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.explosion_sounds = []
        sound_files = [
            "sounds/explosion-1.wav",
            "sounds/explosion-2.wav",
            "sounds/explosion-3.wav",
        ]
        for sound_file in sound_files:
            try:
                self.explosion_sounds.append(pygame.mixer.Sound(sound_file))
            except pygame.error:
                print(f"Error: Sound file '{sound_file}' not found.")
                self.explosion_sounds.append(None)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        sound = random.choice(self.explosion_sounds)
        if sound:
            sound.play()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return ASTEROID_POINTS[0]

        random_angle = random.uniform(20, 50)
        velocity_1 = self.velocity.rotate(random_angle)
        velocity_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = velocity_1 * 1.2

        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2.velocity = velocity_2 * 1.2

        return ASTEROID_POINTS[new_radius // ASTEROID_MIN_RADIUS]
