import pygame
import game_data
import time

class Button:
    def __init__(this, position, folder_name, num_frames, scale_factor=1.0):
        this.images = []
        this.position = position
        this.num_frames = num_frames
        this.current_frame = 0
        this.scale_factor = scale_factor
        this.is_clicked = False
        this.click_time = None
        for i in range(1, num_frames + 1):
            image_path = f'assets\\main-menu\\buttons\\{folder_name}\\{folder_name}{i}.png'
            image = pygame.image.load(image_path)
            scaled_image = pygame.transform.scale(image, (int(image.get_width() * this.scale_factor), int(image.get_height() * this.scale_factor)))
            this.images.append(scaled_image)

    def draw(this, screen):
        screen.blit(this.images[this.current_frame], this.position)

    def handle_click(this):
        # Toggle button animation only if it wasn't already clicked and animation cooldown has passed
        if not this.is_clicked or (this.click_time is not None and time.time() - this.click_time > 2):
            this.current_frame = (this.current_frame + 1) % this.num_frames
            this.is_clicked = True
            this.click_time = time.time()
        else:
            this.is_clicked = False
            this.click_time = None

    def reset(this):
        # Reset button
        this.is_clicked = False
        this.current_frame = 0

class MainMenu:
    def __init__(this, surface):
        this.menu_options = ['Start', 'Credits', 'Quit']
        this.selected_index = 0
        this.start_game = False
        this.surface = surface
        this.musicPlaying = False
        # Initialize button and background images
        button_spacing = 60
        button_start_y = (game_data.SCREEN_HEIGHT - (len(this.menu_options) * button_spacing)) // 2
        this.buttons = [
            Button(
                ((game_data.SCREEN_WIDTH - Button((0, 0), option.lower(), 3, game_data.BUTTON_SCALE).images[0].get_width()) // 2,
                 button_start_y + i * button_spacing),
                option.lower(),
                3,
                game_data.BUTTON_SCALE
            )
            for i, option in enumerate(this.menu_options)
        ]

        this.back_button = Button((20, game_data.SCREEN_HEIGHT - 60), 'back', 3, game_data.BUTTON_SCALE)
        this.show_back_button = False
        this.show_credits_screen = False

        this.bg_img = pygame.image.load('assets\\main-menu\\bg.png')
        this.bg_img = pygame.transform.scale(this.bg_img, (int(this.bg_img.get_width() * game_data.BG_SCALE), int(this.bg_img.get_height() * game_data.BG_SCALE)))
        this.bg_width = this.bg_img.get_width()

        this.pine_img = pygame.image.load('assets\\main-menu\\pine.png')
        this.pine_img = pygame.transform.scale(this.pine_img, (int(this.pine_img.get_width() * game_data.PINE_SCALE), int(this.pine_img.get_height() * game_data.PINE_SCALE)))
        this.pine_width = this.pine_img.get_width()

        this.palm_img = pygame.image.load('assets\\main-menu\\palm.png')
        this.palm_img = pygame.transform.scale(this.palm_img, (int(this.palm_img.get_width() * game_data.PALM_SCALE), int(this.palm_img.get_height() * game_data.PALM_SCALE)))
        this.palm_width = this.palm_img.get_width()

        this.board_img = pygame.image.load('assets\\main-menu\\board.png')
        this.board_img = pygame.transform.scale(this.board_img, (int(this.board_img.get_width() * game_data.BOARD_SCALE), int(this.board_img.get_height() * game_data.BOARD_SCALE)))
        this.board_width = this.board_img.get_width()

        this.speed = 7
        this.bg_x = 0
        this.pine_x = 0
        this.palm_x = 0

        this.bg_y = 0
        this.pine_y = 200
        this.palm_y = 360
        
        this.credits_data = [
            {"name": "Rupen", "github": "https://github.com/hellbuster45"},
            {"name": "Ujjwal", "github": "https://github.com/bionicop"}
        ]
    
    def draw_credits(this):
        this.draw_background_images()

        this.surface.blit(this.board_img, ((game_data.SCREEN_WIDTH - this.board_width) // 2, 50))

        font = pygame.font.Font(None, 35)
        text_y = 110
        rendered_credits = font.render("CREDITS", True, (0, 0, 0))
        this.surface.blit(rendered_credits, ((game_data.SCREEN_WIDTH - rendered_credits.get_width()) // 2, text_y))
        text_y += 80

        for credit in this.credits_data:
            rendered_name = font.render(credit['name'], True, (24, 25, 26))
            this.surface.blit(rendered_name, ((game_data.SCREEN_WIDTH - rendered_name.get_width()) // 4, text_y))

            rendered_link = font.render(credit['github'], True, (220, 20, 60))
            link_rect = rendered_link.get_rect(topleft=((game_data.SCREEN_WIDTH - rendered_link.get_width()) // 4 * 3, text_y))
            this.surface.blit(rendered_link, link_rect.topleft)

            # Check for mouse click and open the link if clicked
            if link_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    import webbrowser
                    webbrowser.open(credit['github'])  # Open the link in a web browser

            text_y += 50

        if this.show_back_button:
            this.back_button.draw(this.surface)

    def draw_menu(this):
        this.draw_background_images()

        if this.show_back_button:
            this.back_button.draw(this.surface)

        for button in this.buttons:
            button.draw(this.surface)
    
    def draw_background_images(this):
        this.surface.blit(this.bg_img, (this.bg_x, this.bg_y))
        this.surface.blit(this.bg_img, (this.bg_x + this.bg_width, this.bg_y))

        this.surface.blit(this.pine_img, (this.pine_x, this.pine_y))
        this.surface.blit(this.pine_img, (this.pine_x + this.pine_width, this.pine_y))

        this.surface.blit(this.palm_img, (this.palm_x, this.palm_y))
        this.surface.blit(this.palm_img, (this.palm_x + this.palm_width, this.palm_y))

        if this.bg_x <= -this.bg_width:
            this.surface.blit(this.bg_img, (this.bg_x + this.bg_width, this.bg_y))
            this.bg_x = 0

        if this.pine_x <= -this.pine_width:
            this.surface.blit(this.pine_img, (this.pine_x + this.pine_width, this.pine_y))
            this.pine_x = 0

        if this.palm_x <= -this.palm_width:
            this.surface.blit(this.palm_img, (this.palm_x + this.palm_width, this.palm_y))
            this.palm_x = 0

        this.bg_x -= this.speed * 0.076
        this.pine_x -= this.speed * 0.17
        this.palm_x -= this.speed * 0.21
    
    def handle_click(this, pos):
        for i, button in enumerate(this.buttons):
            if button.position[0] <= pos[0] <= button.position[0] + button.images[0].get_width() and \
                    button.position[1] <= pos[1] <= button.position[1] + button.images[0].get_height():
                button.handle_click()
                
                if i == 0:  # Start button clicked
                    this.start_game = True
                elif i == 1:  # Credits button clicked
                    this.show_back_button = True  # Show the back button on the Credits screen
                    this.show_credits_screen = True  # Show the Credits screen
                elif i == 2:  # Quit button clicked
                    if button.is_clicked:
                        pygame.quit()
                        quit()
                break

        if this.back_button.position[0] <= pos[0] <= this.back_button.position[0] + this.back_button.images[0].get_width() and this.back_button.position[1] <= pos[1] <= this.back_button.position[1] + this.back_button.images[0].get_height():
            this.back_button.handle_click()
            this.show_back_button = False
            this.show_credits_screen = False