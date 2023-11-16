import pygame
import game_data
import time

class Button:
    def __init__(self, position, folder_name, num_frames, scale_factor=1.0):
        self.images = []
        self.position = position
        self.num_frames = num_frames
        self.current_frame = 0
        self.scale_factor = scale_factor
        self.is_clicked = False
        self.click_time = None

        for i in range(1, num_frames + 1):
            image_path = f'assets\\main-menu\\buttons\\{folder_name}\\{folder_name}{i}.png'
            image = pygame.image.load(image_path)
            scaled_image = pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor)))
            self.images.append(scaled_image)

    def draw(self, screen):
        screen.blit(self.images[self.current_frame], self.position)

    def handle_click(self):
        # Toggle button animation only if it wasn't already clicked and animation cooldown has passed
        if not self.is_clicked or (self.click_time is not None and time.time() - self.click_time > 2):
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.is_clicked = True
            self.click_time = time.time()
        else:
            self.is_clicked = False
            self.click_time = None

    def reset(self):
        # Reset button
        self.is_clicked = False
        self.current_frame = 0

def draw_background_images(screen, bg_img, bg_x, bg_y, bg_width, pine_img, pine_x, pine_y, pine_width, palm_img, palm_x, palm_y, palm_width, speed):
    screen.blit(bg_img, (bg_x, bg_y))
    screen.blit(bg_img, (bg_x + bg_width, bg_y))

    screen.blit(pine_img, (pine_x, pine_y))
    screen.blit(pine_img, (pine_x + pine_width, pine_y))

    screen.blit(palm_img, (palm_x, palm_y))
    screen.blit(palm_img, (palm_x + palm_width, palm_y))

    if bg_x <= -bg_width:
        screen.blit(bg_img, (bg_x + bg_width, bg_y))
        bg_x = 0

    if pine_x <= -pine_width:
        screen.blit(pine_img, (pine_x + pine_width, pine_y))
        pine_x = 0

    if palm_x <= -palm_width:
        screen.blit(palm_img, (palm_x + palm_width, palm_y))
        palm_x = 0

    bg_x -= speed * 0.076
    pine_x -= speed * 0.17
    palm_x -= speed * 0.21

    return bg_x, pine_x, palm_x

class MainMenu:
    def __init__(self):
        self.menu_options = ['Start', 'Credits', 'Quit']
        self.selected_index = 0

        # Initialize button and background images
        button_spacing = 60
        button_start_y = (game_data.SCREEN_HEIGHT - (len(self.menu_options) * button_spacing)) // 2
        self.buttons = [
            Button(
                ((game_data.SCREEN_WIDTH - Button((0, 0), option.lower(), 3, game_data.BUTTON_SCALE).images[0].get_width()) // 2,
                 button_start_y + i * button_spacing),
                option.lower(),
                3,
                game_data.BUTTON_SCALE
            )
            for i, option in enumerate(self.menu_options)
        ]

        self.back_button = Button((20, game_data.SCREEN_HEIGHT - 60), 'back', 3, game_data.BUTTON_SCALE)
        self.show_back_button = False
        self.show_credits_screen = False

        self.bg_img = pygame.image.load('assets\\main-menu\\bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (int(self.bg_img.get_width() * game_data.BG_SCALE), int(self.bg_img.get_height() * game_data.BG_SCALE)))
        self.bg_width = self.bg_img.get_width()

        self.pine_img = pygame.image.load('assets\\main-menu\\pine.png')
        self.pine_img = pygame.transform.scale(self.pine_img, (int(self.pine_img.get_width() * game_data.PINE_SCALE), int(self.pine_img.get_height() * game_data.PINE_SCALE)))
        self.pine_width = self.pine_img.get_width()

        self.palm_img = pygame.image.load('assets\\main-menu\\palm.png')
        self.palm_img = pygame.transform.scale(self.palm_img, (int(self.palm_img.get_width() * game_data.PALM_SCALE), int(self.palm_img.get_height() * game_data.PALM_SCALE)))
        self.palm_width = self.palm_img.get_width()

        self.board_img = pygame.image.load('assets\\main-menu\\board.png')
        self.board_img = pygame.transform.scale(self.board_img, (int(self.board_img.get_width() * game_data.BOARD_SCALE), int(self.board_img.get_height() * game_data.BOARD_SCALE)))
        self.board_width = self.board_img.get_width()

        self.speed = 7
        self.bg_x = 0
        self.pine_x = 0
        self.palm_x = 0

        self.bg_y = 0
        self.pine_y = 200
        self.palm_y = 360
        
        self.credits_data = [
            {"name": "Rupen Kumar", "github": "https://github.com/hellbuster45"},
            {"name": "Ujjwal", "github": "https://github.com/bionicop"}
        ]
    
    def draw_credits(self):
        self.bg_x, self.pine_x, self.palm_x = draw_background_images(screen, self.bg_img, self.bg_x, self.bg_y, self.bg_width, self.pine_img, self.pine_x, self.pine_y, self.pine_width, self.palm_img, self.palm_x, self.palm_y, self.palm_width, self.speed)

        screen.blit(self.board_img, ((game_data.SCREEN_WIDTH - self.board_width) // 2, 50))

        font = pygame.font.Font(None, 35)
        text_y = 110
        rendered_credits = font.render("CREDITS", True, (0, 0, 0))
        screen.blit(rendered_credits, ((game_data.SCREEN_WIDTH - rendered_credits.get_width()) // 2, text_y))
        text_y += 80

        for credit in self.credits_data:
            rendered_name = font.render(credit['name'], True, (24, 25, 26))
            screen.blit(rendered_name, ((game_data.SCREEN_WIDTH - rendered_name.get_width()) // 4, text_y))

            rendered_link = font.render(credit['github'], True, (220, 20, 60))
            link_rect = rendered_link.get_rect(topleft=((game_data.SCREEN_WIDTH - rendered_link.get_width()) // 4 * 3, text_y))
            screen.blit(rendered_link, link_rect.topleft)

            # Check for mouse click and open the link if clicked
            if link_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    import webbrowser
                    webbrowser.open(credit['github'])  # Open the link in a web browser

            text_y += 50

        if self.show_back_button:
            self.back_button.draw(screen)

    def draw_menu(self):
        self.bg_x, self.pine_x, self.palm_x = draw_background_images(screen, self.bg_img, self.bg_x, self.bg_y, self.bg_width, self.pine_img, self.pine_x, self.pine_y, self.pine_width, self.palm_img, self.palm_x, self.palm_y, self.palm_width, self.speed)

        if self.show_back_button:
            self.back_button.draw(screen)

        for button in self.buttons:
            button.draw(screen)

    def handle_click(self, pos):
        for i, button in enumerate(self.buttons):
            if button.position[0] <= pos[0] <= button.position[0] + button.images[0].get_width() and \
                    button.position[1] <= pos[1] <= button.position[1] + button.images[0].get_height():
                button.handle_click()
                if i == 0:  # Start button clicked
                    print("Start button clicked")
                elif i == 1:  # Credits button clicked
                    print("Credits button clicked")
                    self.show_back_button = True  # Show the back button on the Credits screen
                    self.show_credits_screen = True  # Show the Credits screen
                elif i == 2:  # Quit button clicked
                    print("Quit button clicked")
                    if button.is_clicked:
                        pygame.quit()
                        quit()
                break

        if self.back_button.position[0] <= pos[0] <= self.back_button.position[0] + self.back_button.images[0].get_width() and self.back_button.position[1] <= pos[1] <= self.back_button.position[1] + self.back_button.images[0].get_height():
            self.back_button.handle_click()
            print("Back button clicked")
            self.show_back_button = False
            self.show_credits_screen = False

# Initializing pygame and setting up the game window
pygame.init()
screen = pygame.display.set_mode((game_data.SCREEN_WIDTH, game_data.SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True
menu = MainMenu()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                menu.handle_click(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))

    if menu.show_credits_screen:
        menu.draw_credits()
    else:
        menu.draw_menu()

    pygame.display.update()

pygame.quit()