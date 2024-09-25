import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class InitialsInputScreen:
    def __init__(self, screen, font, score):
        self.screen = screen
        self.font = font
        self.score = score
        self.initials = ["_", "_", "_"]  # Start with three underscores
        self.current_index = 0  # Current letter being edited

    def display(self):
        """Display the initials input screen."""
        self.screen.fill("black")

        self.screen.fill("black")
        score_text = self.font.render(f"New High Score: {self.score}", True, "white")
        text = self.font.render(f"Enter Your Initials:", True, "white")
        initials_str = "".join(self.initials)
        initials_text = self.font.render(initials_str, True, "yellow")

        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(initials_text,  (SCREEN_WIDTH // 2 - initials_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if self.current_index < 3:
                    # Handle alphabet input
                    if event.unicode.isalpha():
                        self.initials[self.current_index] = event.unicode.upper()
                        self.current_index += 1
                    elif event.key == pygame.K_BACKSPACE and self.current_index > 0:
                        self.current_index -= 1
                        self.initials[self.current_index] = "_"

                # Check if initials are fully entered
                if self.current_index >= 3 or (event.key == pygame.K_RETURN and "_" not in self.initials):
                    return "".join(self.initials)  # Return the entered initials

        return None
