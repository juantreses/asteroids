import os
import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from gameoverscreen import GameOverScreen
from initialsinputscreen import InitialsInputScreen
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
    high_scores = [('AAA', 0), ('BBB', 0), ('CCC', 0)]

    while True:
        # Initialize game elements
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
                if not player.invincible and asteroid.collides_with(player):
                    player.lose_life()
                    if player.lives <= 0:
                        game_over_screen = GameOverScreen(screen, font, score, high_scores)
                        game_over_screen.display()

                        # Check if the player has a new high score
                        if game_over_screen.is_high_score():
                            initials_input_screen = InitialsInputScreen(screen, font, score)
                            initials = None
                            while initials is None:
                                initials_input_screen.display()  # Keep displaying the initials input screen
                                initials = initials_input_screen.handle_input()  # Get the initials input

                            game_over_screen.add_high_score(initials)
                            high_scores = game_over_screen.high_scores

                        game_over_screen.display()  # Display the updated game over screen
                        game_over_screen.waiting = True  # Reset waiting state
                        while game_over_screen.waiting:
                            restart = game_over_screen.handle_input()
                            if restart:
                                game_over = True
                                break
                        if not game_over:
                            return

                # Check collisions between asteroids and shots
                for shot in shots:
                    if asteroid.collides_with(shot):
                        score += asteroid.split()
                        shot.kill()

            screen.fill("black")

            # Render texts
            lives_text = font.render(f"Lives: {player.lives}", True, "white")
            score_text = font.render(f"Score: {score}", True, "yellow")
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))

            for sprite in drawable:
                sprite.draw(screen)

            pygame.display.flip()

            dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
