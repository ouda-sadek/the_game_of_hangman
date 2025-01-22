import pygame

# Initialize Pygame 
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height) is a tuple 
screen = pygame.display.set_mode((840, 600))
pygame.display.set_caption("THE GAME OF HANGMAN")

#Define color & size
WHITE = (250, 250, 250)

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
    # Define the line color (RGB)
    line_color = line_color = (WHITE)
    for start_pos, end_pos in lines:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Main loop to keep the window open until user closes it
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_line()
    # Display the window
    pygame.display.flip()
pygame.quit()

   