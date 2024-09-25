import os
import sys

import pygame

from asteroidfield import AsteroidField


class TitleScreen:
    def __init__(self, screen, font, updatable, drawable, asteroids, clock):
        self.screen = screen
        self.font = font
        self.updatable = updatable
        self.drawable = drawable
        self.asteroids = asteroids
        self.clock = clock
        self.waiting = True
        self.dt = 0

        music_file = "sounds/intro.mp3"
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: Music file '{music_file}' not found.")

        AsteroidField(1.6, 20, 40)

    def display(self):
        for sprite in self.updatable:
            sprite.update(self.dt)

        self.screen.fill("black")

        # Render title text
        title_text = self.font.render("ASTEROIDS", True, "white")
        start_text = self.font.render("Press any key to start", True, "yellow")

        # Centering the text on the screen
        self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(start_text, (self.screen.get_width() // 2 - start_text.get_width() // 2, 2 * self.screen.get_height() // 3))

        for sprite in self.drawable:
            sprite.draw(self.screen)

        pygame.display.flip()

        self.dt = self.clock.tick(60) / 1000

    def handle_input(self):
        """Wait for player input to start the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.waiting = False
                pygame.mixer.music.stop()
                for sprite in self.updatable:
                    sprite.kill()
                return True

        return False
