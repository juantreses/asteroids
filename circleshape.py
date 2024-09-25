import pygame


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, radius: float):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        """Sub-classes must override this method to draw the shape."""
        pass

    def update(self, dt: float):
        """Sub-classes must override this method to update the shape."""
        pass

    def collides_with(self, other: 'CircleShape') -> bool:
        """Check if this circle collides with another circle."""
        return self.position.distance_to(other.position) < self.radius + other.radius
