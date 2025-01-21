import pygame

pygame.init()

# Define the window size
window_width = 400
window_height = 400

# Create a Pygame window and set the title, ((window_width, window_height) is a tuple 
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Window")

running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

    