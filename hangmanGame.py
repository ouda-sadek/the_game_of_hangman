import pygame
import random
import os

# IInitialize Pygame 
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height) is a tuple
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Define color & size
font = pygame.font.SysFont("arial", 40)
title_font = pygame.font.SysFont("arial", 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
line_color = (WHITE)

# Function to read words from the file and select one randomly
def get_random_word(filename="words.txt"):
    with open(filename, "r") as file:
        words = file.read().splitlines()  
    return random.choice(words).strip()  

# Function  score history
def load_scores(filename="scores.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            scores = file.readlines()
            return [int(score.strip()) for score in scores]  # Convertir les scores en entiers
    return []

    
def save_score(filename="scores.txt", score=0):
    with open(filename, "a") as file:
        file.write(f"{score}\n")

def display_scores(scores):
    if not scores:
        return "No scores yet"
    return "\n".join([f"Game {i+1}: {score} wins" for i, score in enumerate(scores)])

# Set word to guess and list of guessed letters
#WORD = get_random_word()      
victory = 0
lost = 0

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

# Function to draw the board
def draw_board(board, guessed_letters, attempts):
    screen.fill(BLACK)
    draw_line()

    # Show the word to guess
    display_word = " ".join(board)
    word_text = font.render(display_word, True, WHITE)
    screen.blit(word_text, (100, 450))

    # Show already guessed letters
    guessed_text = "Guessed letters: " + " ".join(sorted(guessed_letters))
    guessed_text_surf = font.render(guessed_text, True, WHITE)
    screen.blit(guessed_text_surf, (100, 550))

    # Show remaining attempts
    attempts_text = "Attempts left: {}".format(attempts)
    attempts_text_surf = font.render(attempts_text, True, WHITE)
    screen.blit(attempts_text_surf, (100, 650))

    draw_hangman(6 - attempts)
    pygame.display.flip()

# Main function of the game
def play_game():
    global victory, lost

    WORD = get_random_word()
    attempts = 6
    board = ["_" for _ in range(len(WORD))]
    guessed_letters = set()
    game_over = False

    while not game_over:
        draw_board(board, guessed_letters, attempts)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key)

                if len(guess) == 1 and guess.isalpha() and guess not in guessed_letters:
                    guessed_letters.add(guess)

                    if guess in WORD:
                        for i in range(len(WORD)):
                            if WORD[i] == guess:
                                board[i] = guess
                        
                    else:
                        attempts -= 1
                        if attempts == 0:
                            lost += 1
                            game_over = True
                            break

                if "_" not in board:
                    victory += 1
                    game_over = True
                    break
        
        pygame.time.Clock().tick(100)  

    return True

# function to display the menu
def display_menu():
    global victory, lost
    running = True
    while running:
        screen.fill(BLACK)

        title_text = title_font.render("HANGMAN GAME", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # display options menu
        play_button_text = font.render("Play", True, WHITE)
        results_button_text = font.render("Results", True, WHITE)
        exit_button_text = font.render("Exit", True, WHITE)

        screen.blit(play_button_text, (WIDTH // 2 - play_button_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(results_button_text, (WIDTH // 2 - results_button_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_button_text, (WIDTH // 2 - exit_button_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - play_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + play_button_text.get_width() // 2:
                    if HEIGHT // 2 - 50 < mouse_pos[1] < HEIGHT // 2 + 10:
                        play_game()
                        save_score(score=1 if victory > lost else 0)
                if WIDTH // 2 - results_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + results_button_text.get_width() // 2:
                    if HEIGHT // 2 < mouse_pos[1] < HEIGHT // 2 + 50:
                        results_screen()
                        

                if WIDTH // 2 - exit_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + exit_button_text.get_width() // 2:
                    if HEIGHT // 2 + 50 < mouse_pos[1] < HEIGHT // 2 + 100:
                        running = False
                        pygame.quit()

# Function to display the results of the game
def results_screen():
    global victory, lost
    results_text = load_score()
    running = True
    while running:
        screen.fill(BLACK)

        results_text = font.render(f"You won: {victory} times", True, WHITE)
        screen.blit(results_text, (WIDTH // 2 - results_text.get_width() // 2, HEIGHT // 3))
        save_score(results_text)
        lost_text = font.render(f"You lost: {lost} times", True, WHITE)
        screen.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2))
        save_score(lost_text)
        
        back_text = font.render("Back to Menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5))
        

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - back_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + back_text.get_width() // 2:
                    if HEIGHT // 1.5 < mouse_pos[1] < HEIGHT // 1.5 + 50:
                        running = False

        pygame.time.Clock().tick(60)

# Launch main menu
display_menu()
