import os
import sys

import pygame


class GameOverScreen:
    def __init__(self, screen, font, score):
        self.screen = screen
        self.font = font
        self.score = score
        self.waiting = True

        pygame.mixer.music.stop()
        music_file = "sounds/game_over.mp3"
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: Music file '{music_file}' not found.")
        pygame.mixer.music.play(-1)

    def display(self):
        self.screen.fill("black")
        game_over_text = self.font.render("GAME OVER", True, "red")
        score_text = self.font.render(f"Final Score: {self.score}", True, "yellow")
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, "white")

        # Centering the text on the screen
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, 2 * self.screen.get_height() // 3))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.waiting = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    pygame.mixer.music.stop()
                    self.waiting = False
                    return True

        return False
