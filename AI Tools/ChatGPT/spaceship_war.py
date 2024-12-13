import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship War Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load spaceship image
spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))

# Load laughing dog image
laughing_dog_img = pygame.image.load("laughing_dog.jpeg")
laughing_dog_img = pygame.transform.scale(laughing_dog_img, (200, 200))

# Spaceship properties
spaceship = {
    "x": WIDTH // 2 - 25,
    "y": HEIGHT - 60,
    "width": 50,
    "height": 50,
    "speed": 5,
}

# Bullet properties
bullets = []
BULLET_WIDTH, BULLET_HEIGHT = 10, 20

# Enemy properties
enemies = []
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50

# Game variables
score = 0
game_over = False
enemy_speed_increment = 0.01  # Speed increment per enemy spawn

# Font for displaying text
font = pygame.font.Font(None, 36)

# Function to spawn an enemy
def spawn_enemy():
    global enemy_speed_increment
    enemy = {
        "x": random.randint(0, WIDTH - ENEMY_WIDTH),
        "y": -ENEMY_HEIGHT,
        "speed": random.uniform(1, 3) + (score * enemy_speed_increment),  # Gradually increase speed based on score
    }
    enemies.append(enemy)

# Function to display game over screen with laughing dog
def display_game_over():
    screen.fill(BLACK)  # Clear the screen
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
    screen.blit(laughing_dog_img, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    global game_over, score

    # Spawn enemies periodically
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while True:
        screen.fill(BLACK)  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                spawn_enemy()

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move spaceship
        if keys[pygame.K_LEFT] and spaceship["x"] > 0:
            spaceship["x"] -= spaceship["speed"]
        if keys[pygame.K_RIGHT] and spaceship["x"] < WIDTH - spaceship["width"]:
            spaceship["x"] += spaceship["speed"]
        if keys[pygame.K_SPACE]:
            bullets.append({
                "x": spaceship["x"] + spaceship["width"] // 2 - BULLET_WIDTH // 2,
                "y": spaceship["y"],
            })

        # Update bullets
        for bullet in bullets[:]:
            bullet["y"] -= 5
            if bullet["y"] < 0:
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies[:]:
            enemy["y"] += enemy["speed"]
            if enemy["y"] > HEIGHT:
                enemies.remove(enemy)
                game_over = True

        # Check for collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (
                    bullet["x"] < enemy["x"] + ENEMY_WIDTH and
                    bullet["x"] + BULLET_WIDTH > enemy["x"] and
                    bullet["y"] < enemy["y"] + ENEMY_HEIGHT and
                    bullet["y"] + BULLET_HEIGHT > enemy["y"]
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        # Draw spaceship
        screen.blit(spaceship_img, (spaceship["x"], spaceship["y"]))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, RED, (bullet["x"], bullet["y"], BULLET_WIDTH, BULLET_HEIGHT))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, GREEN, (enemy["x"], enemy["y"], ENEMY_WIDTH, ENEMY_HEIGHT))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check game over
        if game_over:
            display_game_over()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Start the game
if __name__ == "__main__":
    game_loop()
