import pygame
import random
import os 

if not os.path.exists("words.txt"):
    with open("words.txt", "w") as file:
        file.write("python\napple\nbanana\norange\npear\ngrape\nkiwi\nmango\npeach\nplum\nstrawberry\nwatermelon\navocado\nblueberry\ncherry")
    print("File created successfully")

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Pendu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Police
FONT = pygame.font.Font(None, 48)

# Charger les mots depuis le fichier
def load_words():
    if not os.path.exists("mots.txt"):
        with open("mots.txt", "w") as f:
            f.write("pomme\nordinateur\npython\n")
    with open("mots.txt", "r") as f:
        return f.read().splitlines()

# Ajouter un mot au fichier
def add_word(word):
    with open("mots.txt", "a") as f:
        f.write(f"{word}\n")

# Dessin du pendu
def draw_hangman(screen, errors):
    pygame.draw.line(screen, BLACK, (150, 500), (300, 500), 5)  # Base
    if errors > 0:
        pygame.draw.line(screen, BLACK, (200, 500), (200, 200), 5)  # Poteau
    if errors > 1:
        pygame.draw.line(screen, BLACK, (200, 200), (300, 200), 5)  # Barre
    if errors > 2:
        pygame.draw.line(screen, BLACK, (300, 200), (300, 250), 5)  # Corde
    if errors > 3:
        pygame.draw.circle(screen, BLACK, (300, 280), 30, 5)  # Tête
    if errors > 4:
        pygame.draw.line(screen, BLACK, (300, 310), (300, 400), 5)  # Corps
    if errors > 5:
        pygame.draw.line(screen, BLACK, (300, 330), (250, 370), 5)  # Bras gauche
    if errors > 6:
        pygame.draw.line(screen, BLACK, (300, 330), (350, 370), 5)  # Bras droit
    if errors > 7:
        pygame.draw.line(screen, BLACK, (300, 400), (250, 470), 5)  # Jambe gauche
    if errors > 8:
        pygame.draw.line(screen, BLACK, (300, 400), (350, 470), 5)  # Jambe droite

# Jeu principal
def play_game():
    words = load_words()
    word = random.choice(words)
    guessed = ["_"] * len(word)
    attempts = 0
    max_attempts = 8
    guessed_letters = set()
    running = True

    while running:
        screen.fill(WHITE)
        text = FONT.render("Mot : " + " ".join(guessed), True, BLACK)
        screen.blit(text, (50, 50))

        draw_hangman(screen, attempts)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                letter = event.unicode.lower()
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter in word:
                        for i, char in enumerate(word):
                            if char == letter:
                                guessed[i] = letter
                    else:
                        attempts += 1
                        if attempts > max_attempts:
                            running = False

        if "_" not in guessed:
            print("Gagné !")
            break

# Menu principal
def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        title = FONT.render("Jeu du Pendu", True, BLACK)
        play_button = FONT.render("1. Jouer", True, BLACK)
        add_word_button = FONT.render("2. Ajouter un mot", True, BLACK)

        screen.blit(title, (300, 100))
        screen.blit(play_button, (300, 200))
        screen.blit(add_word_button, (300, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game()
                elif event.key == pygame.K_2:
                    word = input("Entrez un mot à ajouter : ")
                    add_word(word)

# Lancer le menu principal
main_menu()
pygame.quit()   