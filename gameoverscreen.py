import os
import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverScreen:
    def __init__(self, screen, font, score, high_scores):
        self.screen = screen
        self.font = font
        self.score = score
        self.high_scores = high_scores
        self.waiting = True

        # Load and play game over music
        pygame.mixer.music.stop()
        music_file = "sounds/game_over.mp3"
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        else:
            print(f"Error: Music file '{music_file}' not found.")

    def display(self):
        """Display the game over screen."""
        self.screen.fill("black")
        game_over_text = self.font.render("GAME OVER", True, "red")
        score_text = self.font.render(f"Final Score: {self.score}", True, "yellow")
        hiscore_text = self.font.render("HIGH SCORES", True, "yellow")
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, "white")

        # Centering the text on the screen
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))
        self.screen.blit(hiscore_text, (SCREEN_WIDTH // 2 - hiscore_text.get_width() // 2, SCREEN_HEIGHT // 3 + 100))

        # Dynamically render high scores
        start_y = SCREEN_HEIGHT // 3 + 150
        spacing = 30
        for i, (initials, score) in enumerate(self.high_scores):
            score_text = self.font.render(f"{i + 1}. {initials} - {score}", True, "yellow")
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, start_y + i * spacing))

        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, start_y + 150))

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

    def is_high_score(self):
        if not self.high_scores:
            return True
        """Check if the current score qualifies for the top 3."""
        return self.score > self.high_scores[-1][1]

    def add_high_score(self, initials):
        for i, (initial, score) in enumerate(self.high_scores):
            if self.score > score:
                self.high_scores.insert(i, (initials, self.score))
                break
        else:
            self.high_scores.append((initials, self.score))

        self.high_scores = self.high_scores[:3]