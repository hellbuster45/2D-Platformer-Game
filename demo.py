import pygame as po
import game_data as c
import math as m
import sys

po.init()
screen = po.display.set_mode((1280, 720))
display = po.Surface((1280 * 0.2, 720 * 0.2))

bg_img = po.image.load('assets\Sunny-land-files\Graphical Assets\environment\Background\\back.png').convert_alpha()
bg_width = bg_img.get_width()
palm_img = po.image.load('assets\Sunny-land-files\Graphical Assets\environment\Props\palm.png').convert_alpha()
palm_width = palm_img.get_width()
pine_img = po.image.load('assets\Sunny-land-files\Graphical Assets\environment\Props\pine.png').convert_alpha()
pine_width = pine_img.get_width()

# game vars
sky_tiles = m.ceil((1280 * 0.2) / bg_width)
palm_tiles = m.ceil((1280 * 0.2) / palm_width)
pine_tiles = m.ceil((1280 * 0.2) / pine_width)
print(sky_tiles, pine_tiles, palm_tiles)
scroll = 0
clock = po.time.Clock()
run = True
while run:
    clock.tick(10)
    display.blit(bg_img, ((bg_width + (scroll * 0.1)), 0))
    for i in range(0, 100):
        if i // 5 == 0:
            display.blit(bg_img, ((i * bg_width) + (scroll * 0.1), 0))
        display.blit(pine_img, ((i * (pine_width - 25) - 30) + (scroll * 0.2), 60))
        display.blit(palm_img, ((i * (palm_width - 20) + (scroll * 0.3), 100)))
    scroll -= 2
    for event in po.event.get():
        if event.type == po.QUIT:
            run = False
    screen.blit(po.transform.scale(display, screen.get_size()), (0, 0))
    po.display.update()    
po.quit()

# import pygame

# # Initialize Pygame
# pygame.init()

# # Create a screen
# screen = pygame.display.set_mode((800, 600))

# # Load the background image
# background = pygame.image.load("assets\Sunny-land-files\Graphical Assets\environment\Background\\back.png")

# # Create a variable to store the background position
# background_x = 0

# # Create a while loop that will run continuously until the game is closed
# while True:

#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()

#     # Draw the background
#     screen.blit(background, (background_x, 0))

#     # Move the background
#     background_x -= 1

#     # If the background is off the screen, reset it to the beginning
#     if background_x < -background.get_width():
#         background_x = 0

#     # Update the screen
#     pygame.display.update()