import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height) is a tuple)
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Game Of Hangman")

# Define color & size
font = pygame.font.SysFont("arial", 40)
title_font = pygame.font.SysFont("arial", 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
line_color = (WHITE)

# Function to read words from the file and select one randomly
def get_random_word(filename="words.txt"):
    with open(filename, "r") as file:
        words = file.read().splitlines()  
    return random.choice(words).strip()  

# Function to add a word to the words.txt file
def add_word_to_file(word, filename="words.txt"):
    with open(filename, "a") as file:
        file.write(f"{word}\n")

# Function to load score history from a file
def load_scores(filename="scores.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            scores = file.readlines()
            # convert scores into an integer
            return [int(score.strip()) for score in scores]

# Function to save a score to the file
def save_scores(filename="scores.txt", score=0):
    with open(filename, "a") as file:
        # save the victory score(1) and the loss score(0)
        file.write(f"{score}\n")

# Function to display the scores
def display_scores(scores):
    if not scores:
        return "No scores yet"
    return "\n".join([f"Game {i+1}: {"Won" if score == 1 else "Lost"}" for i, score in enumerate(scores)])

# Set word to guess and list of guessed letters
victory = 0
lost = 0
# Default difficulty
difficulty = "medium"  

# Function to define and draw the line position with (X, Y)
def draw_line():
    lines = [
        ((100, 400), (400, 400)),
        ((150, 100), (150, 400)),
        ((150, 100), (350, 100)), 
        ((350, 100), (350, 150)),  
        ((200, 100), (150, 150)),
    ]
    for start_pos, end_pos in lines:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Function to draw the hangman based on the number of mistakes made
def draw_hangman(mistakes):
    if mistakes >= 1:
        pygame.draw.circle(screen, line_color, (350, 175), 20)  
    if mistakes >= 2:
        pygame.draw.line(screen, line_color, (350, 195), (350, 250), 5)  
    if mistakes >= 3:
        pygame.draw.line(screen, line_color, (350, 230), (300, 200), 5)  
    if mistakes >= 4:
        pygame.draw.line(screen, line_color, (350, 230), (400, 200), 5)  
    if mistakes >= 5:
        pygame.draw.line(screen, line_color, (350, 250), (300, 300), 5)  
    if mistakes >= 6:
        pygame.draw.line(screen, line_color, (350, 250), (400, 300), 5)  

# Function to draw the board
def draw_board(board, guessed_letters, attempts):
    screen.fill(BLACK)
    draw_line()

    display_word = " ".join(board)
    word_text = font.render(display_word, True, WHITE)
    screen.blit(word_text, (100, 450))

    guessed_text = "Guessed letters: " + " ".join(sorted(guessed_letters))
    guessed_text_surf = font.render(guessed_text, True, WHITE)
    screen.blit(guessed_text_surf, (100, 550))

    attempts_text = "Attempts left: {}".format(attempts)
    attempts_text_surf = font.render(attempts_text, True, WHITE)
    screen.blit(attempts_text_surf, (100, 650))

    draw_hangman(6 - attempts)
    pygame.display.flip()

# Function to define attempts based on difficulty
def get_attempts_for_difficulty(difficulty):
    if difficulty == "easy":
        return 8
    elif difficulty == "medium":
        return 6
    # hard
    else:  
        return 4

# Main function of the game
def play_game():
    global victory, lost, difficulty

    WORD = get_random_word()
    attempts = get_attempts_for_difficulty(difficulty)
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
                            save_scores(score=0)  # Save loss
                            break

                if "_" not in board:
                    victory += 1
                    game_over = True
                    save_scores(score=1)  # Save win
                    break
        
        pygame.time.Clock().tick(100)  

    return True

# Function to display the difficulty menu
def display_difficulty_menu():
    global difficulty
    running = True
    while running:
        screen.fill(BLACK)

        title_text = title_font.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 5))

        easy_button_text = font.render("Easy", True, WHITE)
        medium_button_text = font.render("Medium", True, WHITE)
        hard_button_text = font.render("Hard", True, WHITE)
        back_button_text = font.render("Back to Menu", True, WHITE)

        screen.blit(easy_button_text, (WIDTH // 2 - easy_button_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(medium_button_text, (WIDTH // 2 - medium_button_text.get_width() // 2, HEIGHT // 2))
        screen.blit(hard_button_text, (WIDTH // 2 - hard_button_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(back_button_text, (WIDTH // 2 - back_button_text.get_width() // 2, HEIGHT // 2 + 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - easy_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + easy_button_text.get_width() // 2:
                    if HEIGHT // 2 - 100 < mouse_pos[1] < HEIGHT // 2 - 50:
                        difficulty = "easy"
                        running = False
                if WIDTH // 2 - medium_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + medium_button_text.get_width() // 2:
                    if HEIGHT // 2 < mouse_pos[1] < HEIGHT // 2 + 50:
                        difficulty = "medium"
                        running = False
                if WIDTH // 2 - hard_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + hard_button_text.get_width() // 2:
                    if HEIGHT // 2 + 100 < mouse_pos[1] < HEIGHT // 2 + 150:
                        difficulty = "hard"
                        running = False
                if WIDTH // 2 - back_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + back_button_text.get_width() // 2:
                    if HEIGHT // 2 + 200 < mouse_pos[1] < HEIGHT // 2 + 250:
                        running = False
                        display_menu()

# Function to display the menu
def display_menu():
    global victory, lost
    running = True
    while running:
        screen.fill(BLACK)
        

        title_text = title_font.render("THE GAME HANGMAN", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 5))

        play_button_text = font.render("Play", True, WHITE)
        results_button_text = font.render("Results", True, WHITE)
        add_button_text = font.render("Add Word", True, WHITE)
        exit_button_text = font.render("Exit", True, WHITE)

        screen.blit(play_button_text, (WIDTH // 2 - play_button_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(results_button_text, (WIDTH // 2 - results_button_text.get_width() // 2, HEIGHT // 2))
        screen.blit(add_button_text, (WIDTH // 2 - add_button_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(exit_button_text, (WIDTH // 2 - exit_button_text.get_width() // 2, HEIGHT // 2 + 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - play_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + play_button_text.get_width() // 2:
                    if HEIGHT // 2 - 100 < mouse_pos[1] < HEIGHT // 2 - 50:
                        # Show difficulty menu
                        display_difficulty_menu()  
                        play_game()
                if WIDTH // 2 - results_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + results_button_text.get_width() // 2:
                    if HEIGHT // 2 < mouse_pos[1] < HEIGHT // 2 + 50:
                        results_screen()
                if WIDTH // 2 - add_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + add_button_text.get_width() // 2:
                    if HEIGHT // 2 + 100 < mouse_pos[1] < HEIGHT // 2 + 150:
                        add_word_screen()
                if WIDTH // 2 - exit_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + exit_button_text.get_width() // 2:
                    if HEIGHT // 2 + 200 < mouse_pos[1] < HEIGHT // 2 + 250:
                        running = False
                        pygame.quit()

# Function to allow user to add a word to the words.txt file
def add_word_screen():
    input_word = ""
    typing = True

    while typing:
        screen.fill(BLACK)

        input_text = font.render(f"Enter a word: ", True, WHITE)
        screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 2 - 100))
        word_text = font.render(input_word, True, WHITE)
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - 50))
        back_text = font.render("Back to Menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    # Press Enter to add the word
                    if input_word:
                        add_word_to_file(input_word)
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_word = input_word[:-1]
                else:
                    input_word += pygame.key.name(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - back_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + back_text.get_width() // 2:
                    if HEIGHT // 2 + 100 < mouse_pos[1] < HEIGHT // 2 + 150:
                        typing = False

        pygame.time.Clock().tick(60)

# Function to display the results screen
def results_screen():
    # Load scores from file
    scores = load_scores()  
    running = True
    
    while running:
        
        screen.fill(BLACK)

        results_text = font.render(f"You won: {victory} times", True, WHITE)
        screen.blit(results_text, (WIDTH // 2 - results_text.get_width() // 2, HEIGHT // 3))
        
        lost_text = font.render(f"You lost: {lost} times", True, WHITE)
        screen.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2))
        
        back_text = font.render("Back to Menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.5))

        if scores:
            for i, score in enumerate(scores):
                score_text = font.render(f"Game {i+1}: {"Won" if score == 1 else "Lost"}", True, WHITE)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 1.5 + (i+1) * 40))

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

# Launch the main menu
display_menu()
