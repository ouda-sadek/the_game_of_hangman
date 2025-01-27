import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height) is a tuple)
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Game Of Hangman")

background_image = pygame.image.load(os.path.join("background.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_rect = background_image.get_rect()
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
            # Convertir chaque ligne en une liste : [nom, score (1 ou 0), difficulté]
            return [line.strip().split(",") for line in scores]
    return []
# Function to save a score to the file
def save_scores(player_name, victory, lost, difficulty, filename="scores.txt"):
    # Déterminer le score (1 pour victoire, 0 pour défaite)
    score = 1 if victory > lost else 0
    # Sauvegarder dans le fichier avec format "Nom_du_joueur,victoire/perte,difficulté"
    with open(filename, "a") as file:
        file.write(f"{player_name},{score},{difficulty}\n")

# Function to display the scores
def display_scores(scores):
    if not scores:
        return "No scores yet"
    return "\n".join([f"Game {i+1}: {"Won" if score == 1 else "Lost"}" for i, score in enumerate(scores)])

# Set word to guess and list of guessed letters
victory = 0
lost = 0
# Default difficulty
difficulty = "normal"  
player1_name = ""
player2_name = ""
score_player1 = 0
score_player2 = 0

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
        pygame.draw.line(screen, line_color, start_pos, end_pos, 15)

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
    screen.blit(background_image, (0, 0))
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
    elif difficulty == "normal":
        return 6
    # hard
    else:  
        return 4
def get_player_name():
    input_name = ""
    typing = True

    # Afficher l'écran de saisie du nom du joueur
    while typing:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Texte de la zone de saisie
        input_text = font.render("Enter your name:", True, WHITE)
        screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 2 - 100))
        
        # Affichage du nom saisi
        name_text = font.render(input_name, True, WHITE)
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 - 50))
        
        # Texte pour revenir au menu
        back_text = font.render("Back to Menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    # Si l'utilisateur appuie sur "Enter", valider le nom
                    if input_name:
                        typing = False  # Sortir de la boucle si un nom est saisi
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]  # Supprimer le dernier caractère
                else:
                    input_name += pygame.key.name(event.key)  # Ajouter le caractère saisi

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - back_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + back_text.get_width() // 2:
                    if HEIGHT // 2 + 100 < mouse_pos[1] < HEIGHT // 2 + 150:
                        typing = False  # Sortir de la boucle si "Back to Menu" est cliqué

        pygame.time.Clock().tick(60)  # Limiter la fréquence de rafraîchissement

    return input_name  # Retourner le nom du joueur

# Main function of the game
def play_game():
    global victory, lost, difficulty, player1_name

    player1_name = get_player_name()
    if player1_name is None:
        return False 
    WORD = get_random_word()
    attempts = get_attempts_for_difficulty(difficulty)
    board = ["_" for _ in range(len(WORD))]
    guessed_letters = set()
    game_over = False

    while not game_over:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
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
                            # Save loss
                            save_scores(player1_name, victory, lost, difficulty)
                              
                            break

                if "_" not in board:
                    victory += 1
                    game_over = True
                     # Save win
                    save_scores(player1_name, victory, lost, difficulty)

        pygame.time.Clock().tick(60)  # Control frame rate

    # After the game ends, display the result
    result_text = "You Won!" if victory > lost else "You Lost!"
    result_font = pygame.font.SysFont("arial", 50)
    result_message = result_font.render(result_text, True, "Green" if victory  else "Red")
    
    chosen_word =font.render("chosen word: " + WORD, True, WHITE)
    # Clear the screen and display the result message
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))
    screen.blit(result_message, (WIDTH // 2 - result_message.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(chosen_word, (WIDTH // 2 - chosen_word.get_width() // 2, HEIGHT // 2 + 50))
    # Create "Back to Menu" button
    back_text = font.render("Back to Menu", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
    screen.blit(back_text, back_rect)
    
    pygame.display.flip()

    # Wait for a click on "Back to Menu" or key press to return to menu
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the click is inside the "Back to Menu" button
                if back_rect.collidepoint(mouse_pos):
                    waiting_for_input = False  # Exit loop and go back to menu
            if event.type == pygame.KEYDOWN:
                waiting_for_input = False  # Exit loop and go back to menu

    return True

# Function to display the difficulty menu
def display_difficulty_menu():
    global difficulty
    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

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
                        difficulty = "normal"
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
        screen.blit(background_image, (0, 0))

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
                
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - play_button_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + play_button_text.get_width() // 2:
                    if HEIGHT // 2 - 100 < mouse_pos[1] < HEIGHT // 2 - 50:
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
        screen.blit(background_image, (0, 0))

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

def draw_score_table():
    header = ["Name", "Score", "Difficulty"]
    scores = load_scores()
    if not scores:
        return
    rows = [
        [player1_name, victory, difficulty],
        [player2_name, lost, difficulty]
    ]

    # Coordonnées de départ pour le tableau
    x_start = 100
    y_start = 100
    row_height = 50
    col_widths = [250, 150, 200]  # Largeurs des colonnes
    header_height = 60  # Hauteur de l'en-tête

    # Dessiner l'en-tête du tableau
    pygame.draw.rect(screen, BLACK, (x_start, y_start, sum(col_widths), header_height))
    for idx, header_text in enumerate(header):
        draw_text(header_text, font, WHITE, screen, 
                  (x_start + sum(col_widths[:idx]) + 10, y_start + 10))  # Décalage de 10px pour les bordures

    # Dessiner les lignes du tableau
    y_offset = y_start + header_height
    for row in scores:
        for idx, cell in enumerate(row):
            pygame.draw.rect(screen, (50, 50, 50), 
                             (x_start + sum(col_widths[:idx]), y_offset, col_widths[idx], row_height))
            draw_text(str(cell), font, WHITE, screen, 
                      (x_start + sum(col_widths[:idx]) + 10, y_offset + 10))
        y_offset += row_height

    #pygame.display.flip()
    pygame.time.Clock().tick(60)

def draw_text(text, font, color, surface, position):
    label = font.render(text, True, color)
    surface.blit(label, position)


# Function to display the results screen
def results_screen():
    # Load scores from file
    scores = load_scores()
    running = True
    
    while running:
        
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        draw_score_table()
        back_text = font.render("Back to Menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 250)) 
       
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if WIDTH // 2 - back_text.get_width() // 2 < mouse_pos[0] < WIDTH // 2 + back_text.get_width() // 2:
                    if HEIGHT // 2 + 250 < mouse_pos[1] < HEIGHT // 2 + 300:
                        running = False
                        
        pygame.display.update()
        pygame.time.Clock().tick(60)

# Launch the main menu
display_menu()
pygame.quit()                                                                                                                                                               