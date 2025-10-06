import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        """Moves the paddle vertically and clamps it within the screen bounds."""
        self.y += dy
        # Ensure the paddle stays between the top (0) and bottom edge
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        """Returns the pygame Rect object for collision detection and drawing."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """Simple AI logic: moves the paddle toward the ball's Y position."""
        # If the ball is above the paddle's center, move up
        if ball.y < self.y + (self.height / 2) - 10: # -10 adds a small offset
            self.move(-self.speed, screen_height)
        # If the ball is below the paddle's center, move down
        elif ball.y > self.y + (self.height / 2) + 10: # +10 adds a small offset
            self.move(self.speed, screen_height)
