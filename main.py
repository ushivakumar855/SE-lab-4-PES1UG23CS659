import pygame
import time 
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
# Initialize the sound mixer
pygame.mixer.init() 

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        # --- 1. Event Handling (Always needed) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for Replay Menu Input (Only needed when game is not active)
            if not engine.game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    engine.reset_game(3) # Start Best of 3 (First to 2 points)
                elif event.key == pygame.K_5:
                    engine.reset_game(5) # Start Best of 5 (First to 3 points)
                elif event.key == pygame.K_7:
                    engine.reset_game(7) # Start Best of 7 (First to 4 points)
                elif event.key == pygame.K_ESCAPE:
                    running = False # Exit the game
        
        # --- 2. Game Logic Update ---
        # The engine handles input and updates only if game_active is True
        engine.handle_input()
        engine.update()
        
        # --- 3. Rendering ---
        SCREEN.fill(BLACK)
        engine.render(SCREEN)

        # --- 4. Final Display Update and Tick ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
