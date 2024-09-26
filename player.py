import os

import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, \
    SCREEN_WIDTH, SCREEN_HEIGHT
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.sound_file = "sounds/shot.wav"
        if os.path.exists(self.sound_file):
            self.shot_sound = pygame.mixer.Sound(self.sound_file)
        else:
            print(f"Error: Sound file '{self.sound_file}' not found.")
            self.shot_sound = None
        self.lives = 3  # Set initial lives
        self.invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0
        self.blink_on = True

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if not self.invincible or (self.invincible and self.blink_on):
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        if self.shot_sound:
            self.shot_sound.play()
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        self.shot_cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.invincible:
            self.invincible_timer -= dt
            self.blink_timer -= dt

            # Toggle blink every 0.2 seconds
            if self.blink_timer <= 0:
                self.blink_timer = 0.2  # 200 milliseconds
                self.blink_on = not self.blink_on

            # End invincibility if the timer has run out
            if self.invincible_timer <= 0:
                self.invincible = False
                self.blink_on = True

    def lose_life(self):
        self.lives -= 1
        if self.lives > 0:
            self.respawn()
        else:
            self.kill()

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.invincible = True
        self.invincible_timer = 3
