import pygame as po
import game_data as c
from menu import MainMenu
from characters import Character
from collectibles import Collectible
from level import Level

# Initializing pygame and pygame.mixer
po.init()
po.mixer.init()

class Game:
    def __init__(this):
        # actual screen 
        this.height = c.SCREEN_HEIGHT
        this.width = c.SCREEN_WIDTH
        this.screen = po.display.set_mode((this.width, this.height))
        po.display.set_caption('lol')

        # secondary surface, half of main screen, render everything on this
        this.display = po.Surface((this.width, this.height))
        
        this.musicPlaying = False
        
        # background images
        this.sky = po.image.load('levels\level1\\background_PNGs\sky.png').convert_alpha()
        this.sky_rect = this.sky.get_rect()
        this.s_width = this.sky.get_width()
        
        this.mid_front = po.image.load('levels\level1\\background_PNGs\mid_front.png').convert_alpha()
        this.mid_front_rect = this.mid_front.get_rect()
        this.mf_width = this.mid_front.get_width()
        
        this.mid_back = po.image.load('levels\level1\\background_PNGs\mid_back.png').convert_alpha()
        this.mid_back_rect = this.mid_back.get_rect()
        this.mb_width = this.mid_back.get_width()
        
        this.props = po.image.load('levels\level1\\background_PNGs\props.png').convert_alpha()
        this.props_rect = this.props.get_rect()
        
        this.caves_background = po.image.load('levels\level1\\background_PNGs\caves_background.png').convert_alpha()
        this.caves_background_rect = this.caves_background.get_rect()

    # draw stuff on display surface, then blit display onto main screen..
    def draw(this, obj, dir = 1): 
        if obj.rect.x < c.SCREEN_WIDTH and obj.rect.x >= 0:
            this.display.blit(po.transform.flip(obj.image, dir, False), obj.rect)
            this.screen.blit(po.transform.scale(this.display, this.screen.get_size()), (0, 0))
            
    # draw background images onto display with slight delay for each image (scroll * (any numeric value, according to need)),
    # for parallax effect 
    def draw_background(this, scroll):
        this.display.blit(this.sky, (0 - (scroll * 0.3), 0))
        this.display.blit(this.sky, (this.s_width - (scroll * 0.3), 0))
        this.display.blit(this.mid_back, (0  - (scroll * 0.5), 0))
        this.display.blit(this.mid_back, (this.mb_width  - (scroll * 0.5), 0))
        this.display.blit(this.mid_front, (0  - (scroll * 0.7), 0))
        this.display.blit(this.mid_front, (this.mf_width  - (scroll * 0.7), 0))
        
        # these images don't need to be parallaxed
        this.display.blit(this.caves_background, (0 - scroll, 0))
        this.display.blit(this.props, (0 - scroll, 0))

    # load and play background music, and load sound effects
    def music(this):
        this.jump_fx = po.mixer.Sound('sfx\jump.wav')
        this.jump_fx.set_volume(0.1)
        
        this.item_grab_fx = po.mixer.Sound('sfx\item_grab.wav')
        this.item_grab_fx.set_volume(0.2)

        this.shoot_fx = po.mixer.Sound('sfx\shoot.wav')
        this.shoot_fx.set_volume(0.2)
        
class HealthBar(Game):
    def __init__(this, x, y, health, max_health, game):
        this.x = x
        this.y = y
        this.game = game
        this.health = health
        this.max_health = max_health
    
    def draw(this, health, scroll = 0):
        # update health for the health bar
        this.health = health
            
        # calculate ratio for health
        ratio = this.health / this.max_health
            
        # draw the health bar based on the ratio
        po.draw.rect(this.game.display, (0, 0, 0), ((this.x - 2) + scroll, (this.y - 2) + scroll, 54, 14))
        po.draw.rect(this.game.display, (255, 0, 0), (this.x + scroll, this.y + scroll, 50, 10))
        po.draw.rect(this.game.display, (0, 255, 0), (this.x + scroll, this.y + scroll, 50 * ratio, 10))

# main function with the main game loop   
def main():
    # clock for steady fps
    clock = po.time.Clock()
    game = Game()     
    game.music()
    menu = MainMenu(game.screen)
    # Character( character_type, x-cood, y-cood, speed)
    player = Character('player', 110, 180, 3, 100)
    h_bar = HealthBar(10, 10, player.health, player.max_health, game)
    frog1 = Character('frog', 1392, 224, 3, 100)
    frog2 = Character('frog', 2480, 336, 3, 100)
    frog3 = Character('frog', 3504, 176, 3, 100)
    frog4 = Character('frog', 3792, 368, 3, 100)
    frog5 = Character('frog', 5808, 352, 3, 100)
    frog6 = Character('frog', 5856, 352, 3, 100)
    opossum1 = Character('opossum', 496, 208, 2, 75)
    opossum2 = Character('opossum', 1232, 304, 2, 75)
    opossum3 = Character('opossum', 1824, 304, 2, 75)
    opossum4 = Character('opossum', 2496, 336, 2, 75)
    opossum5 = Character('opossum', 3696, 272, 2, 75)
    opossum6 = Character('opossum', 3904, 288, 2, 75)
    opossum7 = Character('opossum', 4432, 288, 2, 75)
    c.enemy_group.add(
        frog1, frog2, frog3, frog4, frog5, frog6,
        opossum1, opossum2, opossum3, opossum4, opossum5, opossum6, opossum7
    )
    
    # collectibles
    cherry1 = Collectible('cherry', 1184, 176)
    cherry2 = Collectible('cherry', 4016, 128)
    cherry3 = Collectible('cherry', 4288, 240)
    cherry4 = Collectible('cherry', 4416, 128)
    cherry5 = Collectible('cherry', 6160, 288)
    cherry6 = Collectible('cherry', 6176, 288)
    cherry7 = Collectible('cherry', 6192, 288)
    cherry8 = Collectible('cherry', 6208, 288)
    s_cherry1 = Collectible('super_cherry', 2048, 176)
    s_cherry2 = Collectible('super_cherry', 3008, 128)
    s_cherry3= Collectible('super_cherry', 5456, 192)
    c.item_group.add(
        cherry1, cherry2, cherry3, cherry4, cherry5, cherry6, cherry7, cherry8,
        s_cherry1, s_cherry2, s_cherry3
    )
    
    bullet_scale = 0.4
    img = po.image.load(f'assets\\bullet sprites\Laser Sprites\\3.png').convert_alpha()
    image = po.transform.scale(img, (int(img.get_width() * bullet_scale), int(img.get_height() * bullet_scale)))
    
    # level and scrolling
    level = Level('levels\level1\\fulldemo.tmx', game.display, player, scale_factor=1.2)
    screen_scroll = 0
    background_scroll = 0
    
    # main loop
    run = True
    while run:
        clock.tick(70)
        if menu.start_game == False:
            if not menu.musicPlaying: 
                po.mixer.music.load('sfx\Final Fantasy 3 - Cute Little Tozas.mp3')
                po.mixer.music.set_volume(0.1)
                po.mixer.music.play(-1, 0.0)
                menu.musicPlaying = True
            if menu.show_credits_screen:
                menu.draw_credits()
            else:
                menu.draw_menu()
        else:
            if not game.musicPlaying:
                po.mixer.music.load('sfx\C418  - Dog - Minecraft Volume Alpha (320kbps).mp3')
                po.mixer.music.set_volume(0.1)
                po.mixer.music.play(-1, 0.0)
                game.musicPlaying = True
            game.draw_background(background_scroll)
            level.run(player.alive, screen_scroll)
            h_bar.draw(player.health)
            if player.alive:
                # draw and update groups
                for bullet in c.bullet_group:
                    game.draw(bullet, bullet.flip)
                    bullet.update(c.enemy_group, level, screen_scroll, True)
                
                for item in c.item_group:
                    game.draw(item)
                    item.update(player, screen_scroll, game.item_grab_fx)
                
                for enemy in c.enemy_group:
                    e_hBar = HealthBar(enemy.rect.x, enemy.rect.y - 20, enemy.health, enemy.max_health, game)
                    e_hBar.draw(enemy.health)
                    if player.alive:
                        enemy.handle_collision(player = player, level = level)
                    if enemy.cType == 'frog':
                        enemy.AI(player, game, level, screen_scroll, background_scroll, True)
                    else:
                        enemy.AI(player, game, level, screen_scroll, background_scroll)
                    enemy.update()
                    game.draw(enemy, enemy.flip)

            game.draw(player, player.flip)
            po.draw.rect(game.display, (0, 0, 255), player.rect, 3)
            player.update()
            
            # player actions performed only when player is alive
            if player.alive:    
                # retrieve the updated screen scroll values from player.move(), 
                # and also allow player to move 
                screen_scroll = player.move(game, level, background_scroll)

                # for scrolling the background images
                background_scroll -= screen_scroll
                # update player action
                if player.shoot:
                    player.shoot(game.shoot_fx, image, player.isShooting)
                
                if player.inAir:
                    player.update_action(c.CHAR_JUMP)
                    
                if player.move_left or player.move_right:
                    player.update_action(c.CHAR_RUN)
                else:
                    player.update_action(c.CHAR_IDLE)
    
        # event handling
        for event in po.event.get():
            if event.type == po.QUIT:
                run = False
            if event.type == po.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu.handle_click(po.mouse.get_pos())
            
            # key presses
            if event.type == po.KEYDOWN:
                if event.key in (po.K_LEFT, po.K_a):
                    player.move_left = True
                if event.key in (po.K_RIGHT, po.K_d):
                    player.move_right = True
                if event.key in (po.K_x, po.K_LCTRL, po.K_RCTRL):
                    player.isShooting = True
                if event.key in (po.K_LSHIFT, po.K_RSHIFT):
                        player.speed = 5
                if event.key in (po.K_UP, po.K_w, po.K_z) and player.alive == True:
                    player.jump = True                
                    
            # key releases
            if event.type == po.KEYUP:
                if event.key in (po.K_LEFT, po.K_a):
                    player.move_left = False
                if event.key in (po.K_RIGHT, po.K_d):
                    player.move_right = False
                if event.key in (po.K_x, po.K_LCTRL, po.K_RCTRL):
                    player.isShooting = False
                if event.key in (po.K_LSHIFT, po.K_RSHIFT):
                        player.speed = 3
                if event.key in (po.K_UP, po.K_w, po.K_z) and player.alive == True:
                    player.jump = False         
        po.display.update()
    po.quit()
main()