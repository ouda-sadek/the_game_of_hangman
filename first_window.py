import pygame

# Initialize Pygame 
pygame.init()

WIDTH = 840
HEIGHT = 600
clock = pygame.time.Clock()
running = True
# Create a Pygame window and set the size ((window_width, window_height) is a tuple 
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("THE GAME OF HANGMAN")

game_over = False
#Define color & size
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
letter_font = pygame.font.SysFont("arial", 60)
key_color = (WHITE)
game_font = pygame.font.SysFont("arial", 50)
line_color = line_color = (WHITE)
# Define the line position with (X, Y)
def draw_line():
    lines = [
        # Define the first horizontal line
        ((100, 400), (400, 400)),  
        # Define the second vertical line
        ((150, 100), (150, 400)), 
        # Define the third horizontal line
        ((150, 100), (350, 100)),  
        # Define the fourth vertical line
        ((350, 100), (350, 150)),  
        # Define the fifth diagonal line
        ((200, 100), (150, 150))   
    ] 
    for start_pos, end_pos in lines:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Define the word to be guessed
WORD = "pygame"
GUESSED = []

# Define the word to be guessed
def display_guess():
    display_text = ""
    for letter in WORD:
            if letter in GUESSED:
                display_text += f"{letter}"
            else:
                display_text += "_ "
    text = letter_font.render(display_text, True, key_color)
    screen.blit(text, (400, 460)) 

# Main loop to keep the window open until user closes it
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            print (f"{key_name}")
            key_name = pygame.key.name(event.key)
            if key_name.isalpha() and len(key_name) ==1:
                print(f"You pressed {key_name}")
                if key_name not in GUESSED:
                    GUESSED.append(key_name)
                    print(f"Guessed letters: {GUESSED}")
                    if key_name in WORD:
                        print("Correct guess!")
                    else:
                        pygame.draw.circle(screen, line_color,(350, 150), 20)
                        print("Wrong guess!")
                else:
                    print("You've already guessed this letter!")
                    #pygame.draw.line(screen, line_color, (350, 175, 350, 200), 5)
            else:
                print("Invalid letter!")
    draw_line()
    display_guess()
    won = True
    for letter in WORD:
        if letter not in GUESSED:
            won = False
    if won:
        game_over = True
        game_over_message = "You won !!"
    else:
        game_over_message = "You lost !!"
    # Display the window
    pygame.display.flip()
    if game_over:
        screen.fill(BLACK)
        text = game_font.render(game_over_message, True, WHITE)
        text.rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text.rect)
        #pygame.update()
        pygame.display.flip()
        clock.tick(60)
pygame.quit()

   