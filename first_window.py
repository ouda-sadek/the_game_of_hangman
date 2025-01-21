import pygame


# Initialize Pygame 
pygame.init()

# Create a Pygame window and set the size ((window_width, window_height) is a tuple 
screen = pygame.display.set_mode((840, 600))
pygame.display.set_caption("Pygame Window")


# Define the line color and starting and ending positions
#Define the line position with (X, Y)
start_pos = (100, 400)
end_pos = (400, 400)

# Define the line color (RGB)
line_color = line_color = (255, 255, 255)

# Draw a line on the screen
pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Define a second line
start_pos = (150, 100)
end_pos = (150, 400)
pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Define a third line
start_pos = (150, 100)
end_pos = (350, 100)
pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Define a fourth line
start_pos = (350, 100)
end_pos = (350, 150)
pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Define a fifth line
start_pos = (200, 100)
end_pos = (150, 150)
pygame.draw.line(screen, line_color, start_pos, end_pos, 5)

# Display the window
pygame.display.flip()

# Main loop to keep the window open until user closes it
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

   