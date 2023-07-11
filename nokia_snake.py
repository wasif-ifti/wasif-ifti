import pygame
import random

# Initialize the game
pygame.init()

# Set up the game window
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up the colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Set up the game variables
cell_size = 20
grid_width = window_width // cell_size
grid_height = window_height // cell_size
snake_speed = 10

# Set up the snake and food
snake_head = [grid_width // 2, grid_height // 2]
snake_body = [[snake_head[0], snake_head[1] + 1], [snake_head[0], snake_head[1] + 2]]
snake_direction = 'UP'
snake_change_to = snake_direction

food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
food_spawn = True

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game levels
levels = {
    1: {'speed': 10, 'score': 5},
    2: {'speed': 15, 'score': 10},
    3: {'speed': 20, 'score': 15}
}
current_level = 1
score = 0

# Function to display the score and level
def show_score_level():
    font = pygame.font.SysFont("Arial", 18)
    score_text = font.render("Score: " + str(score), True, white)
    level_text = font.render("Level: " + str(current_level), True, white)
    window.blit(score_text, (10, 10))
    window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

# Function to display the game over screen
def game_over():
    font = pygame.font.SysFont("Times New Roman", 36)
    game_over_text = font.render("GAME OVERA", True, red)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (window_width // 2, window_height // 2)
    window.blit(game_over_text, game_over_rect)
    show_score_level()
    pygame.display.flip()
    pygame.time.delay(2000)

    # Reset the game variables
    global snake_head, snake_body, snake_direction, snake_change_to, food_pos, food_spawn, score, current_level
    snake_head = [grid_width // 2, grid_height // 2]
    snake_body = [[snake_head[0], snake_head[1] + 1], [snake_head[0], snake_head[1] + 2]]
    snake_direction = 'UP'
    snake_change_to = snake_direction
    food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
    food_spawn = True
    score = 0
    current_level = 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_change_to = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_change_to = 'RIGHT'

    # Validate the direction change
    if (snake_change_to == 'UP' and snake_direction != 'DOWN') or \
            (snake_change_to == 'DOWN' and snake_direction != 'UP') or \
            (snake_change_to == 'LEFT' and snake_direction != 'RIGHT') or \
            (snake_change_to == 'RIGHT' and snake_direction != 'LEFT'):
        snake_direction = snake_change_to

    # Move the snake
    if snake_direction == 'UP':
        snake_head[1] -= 1
    elif snake_direction == 'DOWN':
        snake_head[1] += 1
    elif snake_direction == 'LEFT':
        snake_head[0] -= 1
    elif snake_direction == 'RIGHT':
        snake_head[0] += 1

    # Check if the snake hits the wall
    if snake_head[0] < 0 or snake_head[0] >= grid_width or snake_head[1] < 0 or snake_head[1] >= grid_height:
        game_over()

    # Check if the snake hits itself
    if snake_head in snake_body[1:]:
        game_over()

    # Check if the snake eats the food
    if snake_head == food_pos:
        score += 1
        food_spawn = False
        snake_body.append([])
        if score >= levels[current_level]['score']:
            current_level += 1
            if current_level > len(levels):
                current_level = len(levels)
            snake_speed = levels[current_level]['speed']

    # Spawn new food if necessary
    if not food_spawn:
        while True:
            food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
            if food_pos not in snake_body:
                food_spawn = True
                break

    # Update the snake's body
    snake_body.insert(0, list(snake_head))
    if len(snake_body) > score + 1:
        snake_body.pop()

    # Clear the game window
    window.fill(black)

    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(window, green, (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size))

    # Draw the food
    pygame.draw.rect(window, red, (food_pos[0] * cell_size, food_pos[1] * cell_size, cell_size, cell_size))

    # Draw the walls
    wall_color = blue
    wall_thickness = 2
    pygame.draw.rect(window, wall_color, (0, 0, window_width, wall_thickness))
    pygame.draw.rect(window, wall_color, (0, 0, wall_thickness, window_height))
    pygame.draw.rect(window, wall_color, (0, window_height - wall_thickness, window_width, wall_thickness))
    pygame.draw.rect(window, wall_color, (window_width - wall_thickness, 0, wall_thickness, window_height))

    # Display the score and level
    show_score_level()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(snake_speed)

# Quit the game
pygame.quit()
