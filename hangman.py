import pygame
import random

# Initialize Pygame 
pygame.init()

# Define window dimensions and initialize Pygame clock
WIDTH = 840
HEIGHT = 600
clock = pygame.time.Clock()
running = True

# Create a Pygame window and set the size ((window_width, window_height) is a tuple
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE GAME OF HANGMAN")

game_over = False

#Define color & size
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
letter_font = pygame.font.SysFont("arial", 60)
key_color = (WHITE)
game_font = pygame.font.SysFont("arial", 50)
line_color = (WHITE)

# Function to define and draw the line position with (X, Y)
def draw_line():
    lines = [
        # Define the first horizontal line " bottom horizontal line"
        ((100, 400), (400, 400)),
        # Define the second vertical line "vertical post"  
        ((150, 100), (150, 400)),
        # Define the third horizontal line " horizontal bar"
        ((150, 100), (350, 100)), 
         # Define the fourth vertical line "top vertical line"
        ((350, 100), (350, 150)),  
        # Define the fifth diagonal line
        ((200, 100), (150, 150)),
        
    ]
    
    for start_pos, end_pos in lines:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Function to draw the hangman based on the number of mistakes made
def draw_hangman(mistakes):
    if mistakes >= 1:
        # head
        pygame.draw.circle(screen, line_color, (350, 175), 20)  
    if mistakes >= 2:
        # body
        pygame.draw.line(screen, line_color, (350, 195), (350, 250), 5)  
    if mistakes >= 3:
        # left arm
        pygame.draw.line(screen, line_color, (350, 230), (300, 200), 5)  
    if mistakes >= 4:
       # right arm
        pygame.draw.line(screen, line_color, (350, 230), (400, 200), 5)  
    if mistakes >= 5:
        # left leg
        pygame.draw.line(screen, line_color, (350, 250), (300, 300), 5)  
    if mistakes >= 6:
        # right leg
        pygame.draw.line(screen, line_color, (350, 250), (400, 300), 5)  

# Function to read words from the file and select one randomly
def get_random_word(filename="words.txt"):
    with open(filename, "r") as file:
        words = file.read().splitlines()  
    return random.choice(words).strip()  

# Set word to guess and list of guessed letters
WORD = get_random_word() 
GUESSED = []
mistakes = 0

# Function to display the word with the guessed letters
def display_guess():
    display_text = ""
    for letter in WORD:
        if letter in GUESSED:
            display_text += f"{letter} "
        else:
            display_text += "_ "
    text = letter_font.render(display_text, True, key_color)
    screen.blit(text, (100, 460))

# Main game loop to keep the window open until user closes it
while running:
    # Event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            
            if key_name.isalpha() and len(key_name) == 1:
                if key_name not in GUESSED:
                    GUESSED.append(key_name)
                    if key_name in WORD:
                        print("Correct guess!")
                    else:
                        mistakes += 1
                        print("Wrong guess!")
                else:
                    print("You've already guessed this letter!")
            else:
                print("Invalid letter!")
    
    # Draw the structure of the hanged man
    screen.fill(BLACK)
    draw_line()
    draw_hangman(mistakes)
    display_guess()
    
   # Checking the victory or defeat condition
    won = all(letter in GUESSED for letter in WORD)
    if won:
        game_over = True
        game_over_message = "You won !!"
    elif mistakes >= 6:
        game_over = True
        game_over_message = "You lost !!"
    
    # Show game end message
    if game_over:
        screen.fill(BLACK)
        text = game_font.render(game_over_message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
