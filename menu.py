import pygame
import os

# Initialize Pygame
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height)) is a tuple
WIDTH  = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("THE GAME OF HANGMAN")

# Define colors
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
 
 # Function to display the main menu screen
def display_menu():
    screen.fill(BLACK)
    title_text = pygame.font.SysFont("arial", 50).render("Welcome to the game of hangman", True, WHITE)
    screen.blit(title_text, ((WIDTH  - title_text.get_width()) // 2, 100))
    play_button_text = pygame.font.SysFont("arial", 40).render("Play", True, WHITE)
    screen.blit(play_button_text, (WIDTH // 2 - play_button_text.get_width() // 2, HEIGHT // 2 - 50))
    score_button_text = pygame.font.SysFont("arial", 40).render("Score", True, WHITE)
    screen.blit(score_button_text, (WIDTH // 2 - score_button_text.get_width() // 2, HEIGHT // 2))
    add_button_text = pygame.font.SysFont("arial", 40).render("Add new word", True, WHITE)
    screen.blit(add_button_text, (WIDTH // 2 - add_button_text.get_width() // 2, HEIGHT // 2 + 50))
    change_button_text = pygame.font.SysFont("arial", 40).render("Change word", True, WHITE)
    screen.blit(change_button_text, (WIDTH // 2 - change_button_text.get_width() // 2, HEIGHT // 2 + 100))
    exit_button_text = pygame.font.SysFont("arial", 40).render("Exit", True, WHITE)
    screen.blit(exit_button_text, (WIDTH // 2 - exit_button_text.get_width() // 2, HEIGHT // 2 + 150))
play_button_text = "Play"
score_button_text = "Score"
add_button_text = "Add new word"
change_button_text = "Change"
exit_button_text = "Exit"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_text.collidepoint(mouse_pos):
                os.system("hangman.py")
            if score_button_text.collidepoint(mouse_pos):
                print("Scoreboard")
                os.system("scoreboard.py")
            if add_button_text.collidepoint(mouse_pos):
                print("Add new word")
                os.system("add_word.py")
            if change_button_text.collidepoint(mouse_pos):
                print("Change word")
                os.system("change_word.py")
            if exit_button_text.collidepoint(mouse_pos):
                running = False

    display_menu()
    pygame.display.update()
    #pygame.time.delay(100)

pygame.quit()