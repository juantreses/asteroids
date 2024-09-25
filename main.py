import os

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from gameoverscreen import GameOverScreen
from player import Player
from shot import Shot
from titlescreen import TitleScreen


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0

    while True:
        # initialize game elements
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = updatable
        Shot.containers = (shots, updatable, drawable)

        score = 0

        title_screen = TitleScreen(screen, font, updatable, drawable, asteroids, clock)
        # Display title screen until player presses a key
        while title_screen.waiting:
            title_screen.display()
            title_screen.handle_input()

        # Load and play background music
        music_file = "sounds/music.mp3"
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: Music file '{music_file}' not found.")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Add player after the title screen
        Player.containers = (updatable, drawable)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        AsteroidField()

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            for sprite in updatable:
                sprite.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_over_screen = GameOverScreen(screen, font, score)
                    game_over_screen.display()

                    while game_over_screen.waiting:
                        restart = game_over_screen.handle_input()
                        if restart:
                            game_over = True
                            break
                    if not game_over:
                        return

                for shot in shots:
                    if asteroid.collides_with(shot):
                        score += asteroid.split()
                        shot.kill()

            screen.fill("black")

            score_text = font.render(f"Score: {score}", True, "yellow")
            screen.blit(score_text, (10, 10))

            for sprite in drawable:
                sprite.draw(screen)

            pygame.display.flip()

            dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
