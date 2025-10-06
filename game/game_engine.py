import pygame
import numpy as np
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        
        # Initialize sound effects
        self.init_sounds()

        self.player_score = 0
        self.ai_score = 0
        self.font_score = pygame.font.SysFont("Arial", 30)
        # Using a larger, impactful font for the Game Over message
        self.font_game_over = pygame.font.SysFont("Impact", 72)
        self.font_menu = pygame.font.SysFont("Arial", 28)

        # State variables
        self.MAX_SCORE = 5 # Default best of 9 (first to 5 wins)
        self.game_active = True
        self.winner = None

    def init_sounds(self):
        """Initialize sound effects programmatically"""
        try:
            # Create simple beep sounds using numpy
            sample_rate = 22050
            
            # Paddle hit sound (higher pitch, short)
            duration_paddle = 0.1
            frequency_paddle = 440  # A note
            t = np.linspace(0, duration_paddle, int(sample_rate * duration_paddle))
            paddle_wave = np.sin(2 * np.pi * frequency_paddle * t)
            paddle_wave = (paddle_wave * 32767).astype(np.int16)
            paddle_stereo = np.column_stack((paddle_wave, paddle_wave))
            self.paddle_sound = pygame.sndarray.make_sound(paddle_stereo)
            self.paddle_sound.set_volume(0.3)
            
            # Wall bounce sound (mid pitch, short)
            duration_wall = 0.08
            frequency_wall = 330  # E note
            t = np.linspace(0, duration_wall, int(sample_rate * duration_wall))
            wall_wave = np.sin(2 * np.pi * frequency_wall * t)
            wall_wave = (wall_wave * 32767).astype(np.int16)
            wall_stereo = np.column_stack((wall_wave, wall_wave))
            self.wall_sound = pygame.sndarray.make_sound(wall_stereo)
            self.wall_sound.set_volume(0.2)
            
            # Score sound (lower pitch, longer)
            duration_score = 0.3
            frequency_score = 220  # A note (lower octave)
            t = np.linspace(0, duration_score, int(sample_rate * duration_score))
            score_wave = np.sin(2 * np.pi * frequency_score * t)
            # Add fade out
            fade = np.linspace(1, 0, len(score_wave))
            score_wave = score_wave * fade
            score_wave = (score_wave * 32767).astype(np.int16)
            score_stereo = np.column_stack((score_wave, score_wave))
            self.score_sound = pygame.sndarray.make_sound(score_stereo)
            self.score_sound.set_volume(0.4)
            
            print("✓ Sound effects initialized successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize sounds: {e}")
            # Create dummy sounds that do nothing
            self.paddle_sound = None
            self.wall_sound = None
            self.score_sound = None
    
    def set_ball_sounds(self):
        """Pass sound effects to the ball object"""
        self.ball.wall_sound = self.wall_sound
        self.ball.paddle_sound = self.paddle_sound

    def handle_input(self):
        # Only process input if the game is active
        if self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        if self.game_active:
            # Ensure ball has sound references
            self.set_ball_sounds()
            
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            # Check for scoring (point scored triggers ball reset)
            if self.ball.x <= 0:
                self.ai_score += 1
                # Play score sound
                if self.score_sound:
                    self.score_sound.play()
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                # Play score sound
                if self.score_sound:
                    self.score_sound.play()
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)
            self.check_win()

    def check_win(self):
        """Checks for win condition based on the 'Best of X' system."""
        # Calculate the score required to win (e.g., Best of 5 requires 3 points)
        score_to_win = (self.MAX_SCORE // 2) + 1
        
        if self.player_score >= score_to_win:
            self.game_active = False
            self.winner = "Player"
        elif self.ai_score >= score_to_win:
            self.game_active = False
            self.winner = "AI"

    def reset_game(self, new_max_score):
        """Resets scores, ball, and starts a new game with a new max score."""
        self.player_score = 0
        self.ai_score = 0
        self.MAX_SCORE = new_max_score
        self.game_active = True
        self.winner = None
        self.ball.reset()
        
    def render(self, screen):
        # Draw paddles and center line
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
        
        # Only draw the ball if the game is active
        if self.game_active:
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            

        # Draw score
        player_text = self.font_score.render(str(self.player_score), True, WHITE)
        ai_text = self.font_score.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw Game Over message and menu if the game is over
        if not self.game_active:
            # Determine score needed for display
            score_to_win = (self.MAX_SCORE // 2) + 1
            message = f"{self.winner} Wins! (First to {score_to_win} points)"
            
            # 1. Winner Message
            text_surface = self.font_game_over.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 80))
            screen.blit(text_surface, text_rect)
            
            # 2. Menu Options
            menu_options = [
                ("3: Best of 3 (First to 2 points)", pygame.K_3),
                ("5: Best of 5 (First to 3 points)", pygame.K_5),
                ("7: Best of 7 (First to 4 points)", pygame.K_7),
                ("ESC: Exit", pygame.K_ESCAPE)
            ]
            
            y_offset = self.height // 2 
            for option_text, _ in menu_options:
                option_surface = self.font_menu.render(option_text, True, WHITE)
                option_rect = option_surface.get_rect(center=(self.width // 2, y_offset))
                screen.blit(option_surface, option_rect)
                y_offset += 40
