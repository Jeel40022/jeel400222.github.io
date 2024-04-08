import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set the desired frame rate (in milliseconds)
frame_rate = 100

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

# Load sound effects
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("food_G1U6tlb.mp3")

# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(window_width // 2, window_height // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.score = 0

    def move(self):
        x, y = self.positions[0]

        if self.direction == "UP":
            y -= 10
        elif self.direction == "DOWN":
            y += 10
        elif self.direction == "LEFT":
            x -= 10
        elif self.direction == "RIGHT":
            x += 10

        self.positions.insert(0, (x, y))

        if len(self.positions) > self.size:
            self.positions.pop()

    def change_direction(self, direction):
        if (
            direction == "UP" and self.direction != "DOWN"
            or direction == "DOWN" and self.direction != "UP"
            or direction == "LEFT" and self.direction != "RIGHT"
            or direction == "RIGHT" and self.direction != "LEFT"
        ):
            self.direction = direction

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, green, (position[0], position[1], 10, 10))

    def check_collision(self):
        if (
            self.positions[0][0] < 0
            or self.positions[0][0] >= window_width
            or self.positions[0][1] < 0
            or self.positions[0][1] >= window_height
        ):
            return True

        for position in self.positions[1:]:
            if position == self.positions[0]:
                return True

        return False

    def check_food_collision(self, food):
        if self.positions[0] == food.position:
            self.size += 1
            self.score += 1
            eat_sound.play()
            return True

        return False

# Define the Food class
class Food:
    def __init__(self):
        self.position = (
            random.randint(0, (window_width // 10) - 1) * 10,
            random.randint(0, (window_height // 10) - 1) * 10,
        )

    def draw(self):
        pygame.draw.rect(window, red, (self.position[0], self.position[1], 10, 10))

# Create instances of the Snake and Food classes
snake = Snake()
food = Food()

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Load and display high score
high_score = 0
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read().strip().split(":")[1])
except FileNotFoundError:
    high_score = 0
except ValueError:
    print("Invalid high score format in the file. Resetting high score to 0.")

# Define achievements
achievements = {
    "First_Food_Eaten": False,
    "10_Food_Eaten": False,
    "High_Score_10": False,
    "High_Score_50": False,
}

def check_achievements():
    if snake.score >= 1 and not achievements["First_Food_Eaten"]:
        achievements["First_Food_Eaten"] = True
        print("Achievement Unlocked: First Food Eaten")
    if snake.score >= 10 and not achievements["10_Food_Eaten"]:
        achievements["10_Food_Eaten"] = True
        print("Achievement Unlocked: 10 Food Eaten")
    if snake.score >= 10 and not achievements["High_Score_10"]:
        achievements["High_Score_10"] = True
        print("Achievement Unlocked: High Score 10 (High Score: {})".format(high_score))
    if snake.score >= 50 and not achievements["High_Score_50"]:
        achievements["High_Score_50"] = True
        print("Achievement Unlocked: High Score 50 (High Score: {})".format(high_score))


def render_score():
    score_text = font.render("Score: " + str(snake.score), True, white)  # Display snake.score instead of a separate score variable
    score_text_rect = score_text.get_rect()
    score_text_rect.topleft = (10, 10)  # Position the score at the top left corner of the window
    window.blit(score_text, score_text_rect)

    high_score_text = font.render("High Score: " + str(high_score), True, white)
    high_score_text_rect = high_score_text.get_rect()
    high_score_text_rect.topright = (window_width - 10, 10)
    window.blit(high_score_text, high_score_text_rect)

def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write("High score: " + str(high_score))


# Game loop
running = True
clock = pygame.time.Clock()
while running:
    window.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")
    
    snake.move()

    if snake.check_collision():
        update_high_score(snake.score)
        running = False

    if snake.check_food_collision(food):
        food = Food()
        check_achievements()  # Check for achievements after eating food
        
    # Render the score board
    render_score()

    snake.draw()
    food.draw()

    pygame.display.update()
    clock.tick(20)
    
    pygame.time.delay(frame_rate)

# Game over
pygame.quit()