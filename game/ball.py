import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # Sound effects (will be set by game engine)
        self.wall_sound = None
        self.paddle_sound = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top/bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            # Play wall bounce sound
            if self.wall_sound:
                self.wall_sound.play()

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        # --- Robust Collision Check ---
        
        # Collision with Player Paddle (on the left side)
        if ball_rect.colliderect(player.rect()):
            # Check if the ball is moving LEFT (towards the paddle)
            if self.velocity_x < 0:
                self.velocity_x *= -1
                # Play paddle hit sound
                if self.paddle_sound:
                    self.paddle_sound.play()

        # Collision with AI Paddle (on the right side)
        if ball_rect.colliderect(ai.rect()):
            # Check if the ball is moving RIGHT (towards the paddle)
            if self.velocity_x > 0:
                self.velocity_x *= -1
                # Play paddle hit sound
                if self.paddle_sound:
                    self.paddle_sound.play()
        # ------------------------------

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1 # Flips direction on reset
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
