import pygame as po
from button import Button
import game_data as c
from pytmx.util_pygame import load_pygame
from characters import Character
from collectibles import Collectible
from level import Level

po.init()
po.mixer.init()
# po.mixer.music.load('sfx\Final Fantasy 3 - Cute Little Tozas.mp3')
# po.mixer.music.set_volume(0.05)
# po.mixer.music.play(-1, 0.0, 3000)
class Game:
    def __init__(this):
        # actual screen 
        this.height = c.SCREEN_HEIGHT
        this.width = c.SCREEN_WIDTH
        this.screen = po.display.set_mode((this.width, this.height))
        po.display.set_caption('lol')

        # secondary surface, half of main screen, render everything on this
        this.display = po.Surface((this.width, this.height))
        
        # background images
        this.sky = po.image.load('levels\level1\\background_PNGs\sky.png').convert_alpha()
        this.sky_rect = this.sky.get_rect()
        this.sky = po.transform.scale(this.sky, (int(this.sky_rect.width * c.SCALE_FACTOR), int(this.sky_rect.height * c.SCALE_FACTOR)))
        this.s_width = this.sky.get_width()
        
        this.mid_front = po.image.load('levels\level1\\background_PNGs\mid_front.png').convert_alpha()
        this.mid_front_rect = this.mid_front.get_rect()
        this.mid_front = po.transform.scale(this.mid_front, (int(this.mid_front_rect.width * c.SCALE_FACTOR), int(this.mid_front_rect.height * c.SCALE_FACTOR)))
        this.mf_width = this.mid_front.get_width()
        
        this.mid_back = po.image.load('levels\level1\\background_PNGs\mid_back.png').convert_alpha()
        this.mid_back_rect = this.mid_back.get_rect()
        this.mid_back = po.transform.scale(this.mid_back, (int(this.mid_back_rect.width * c.SCALE_FACTOR), int(this.mid_back_rect.height * c.SCALE_FACTOR)))
        this.mb_width = this.mid_back.get_width()
        
        this.props = po.image.load('levels\level1\\background_PNGs\props.png').convert_alpha()
        this.props_rect = this.props.get_rect()
        this.props = po.transform.scale(this.props, (int(this.props_rect.width * c.SCALE_FACTOR), int(this.props_rect.height * c.SCALE_FACTOR)))
        
        this.caves_background = po.image.load('levels\level1\\background_PNGs\caves_background.png').convert_alpha()
        this.caves_background_rect = this.caves_background.get_rect()
        this.caves_background = po.transform.scale(this.caves_background, (int(this.caves_background_rect.width * c.SCALE_FACTOR), int(this.caves_background_rect.height * c.SCALE_FACTOR)))

    def draw(this, obj, dir = 1):
        this.display.blit(po.transform.flip(obj.image, dir, False), obj.rect)
        this.screen.blit(po.transform.scale(this.display, this.screen.get_size()), (0, 0))
    
    def menu_background(this):
        this.display.blit(this.sky, (0, 0))
        this.display.blit(this.mid_front, (0, 75))
        this.screen.blit(po.transform.scale(this.display, this.screen.get_size()), (0, 0))
        
    def draw_background(this, scroll):
        # images repeated for parallax effect
        this.display.blit(this.sky, (0 - (scroll * 0.3), 0))
        this.display.blit(this.sky, (this.s_width - (scroll * 0.3), 0))
        this.display.blit(this.mid_back, (0  - (scroll * 0.5), 0))
        this.display.blit(this.mid_back, (this.mb_width  - (scroll * 0.5), 0))
        this.display.blit(this.mid_front, (0  - (scroll * 0.7), 0))
        this.display.blit(this.mid_front, (this.mf_width  - (scroll * 0.7), 0))
        
        # only needed once
        this.display.blit(this.caves_background, (0 - scroll, 0))
        this.display.blit(this.props, (0 - scroll, 0))

    def music(this):
        po.mixer.music.load('sfx\Retroland_Recital.mp3')
        po.mixer.music.set_volume(0.1)
        po.mixer.music.play(-1, 0.0, 3000)
        
        this.jump_fx = po.mixer.Sound('sfx\jump.wav')
        this.jump_fx.set_volume(0.2)

        this.enemy_jump_fx = po.mixer.Sound('sfx\enemy_jump.wav')
        this.enemy_jump_fx.set_volume(0.1)

        this.hitHurt_fx = po.mixer.Sound('sfx\hitHurt.wav')
        this.hitHurt_fx.set_volume(0.1)

        this.death_fx = po.mixer.Sound('sfx\death.wav')
        this.death_fx.set_volume(0.1)
        
        this.item_grab_fx = po.mixer.Sound('sfx\item_grab.wav')
        this.item_grab_fx.set_volume(0.1)

        this.shoot_fx = po.mixer.Sound('sfx\shoot.wav')
        this.shoot_fx.set_volume(0.1)
        
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
   
def main():
    # clock for steady fps
    clock = po.time.Clock()
    game = Game()     
    game.music()
    
    # Character( character_type, x-cood, y-cood, speed)
    player = Character('player', 110, 180, 3, 100)
    h_bar = HealthBar(10, 10, player.health, player.max_health, game)
    frog1 = Character('frog', 1392 * c.SCALE_FACTOR, 224 * c.SCALE_FACTOR, 3, 100)
    frog2 = Character('frog', 2480 * c.SCALE_FACTOR, 336 * c.SCALE_FACTOR, 3, 100)
    frog3 = Character('frog', 3504 * c.SCALE_FACTOR, 176 * c.SCALE_FACTOR, 3, 100)
    frog4 = Character('frog', 3792 * c.SCALE_FACTOR, 368 * c.SCALE_FACTOR, 3, 100)
    frog5 = Character('frog', 5808 * c.SCALE_FACTOR, 352 * c.SCALE_FACTOR, 3, 100)
    frog6 = Character('frog', 5856 * c.SCALE_FACTOR, 352 * c.SCALE_FACTOR, 3, 100)
    opossum1 = Character('opossum', 496 * c.SCALE_FACTOR, 208 * c.SCALE_FACTOR, 2, 75)
    opossum2 = Character('opossum', 1232 * c.SCALE_FACTOR, 304 * c.SCALE_FACTOR, 2, 75)
    opossum3 = Character('opossum', 1824 * c.SCALE_FACTOR, 304 * c.SCALE_FACTOR, 2, 75)
    opossum4 = Character('opossum', 2496 * c.SCALE_FACTOR, 336 * c.SCALE_FACTOR, 2, 75)
    opossum5 = Character('opossum', 3696 * c.SCALE_FACTOR, 272 * c.SCALE_FACTOR, 2, 75)
    opossum6 = Character('opossum', 3904 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR, 2, 75)
    opossum7 = Character('opossum', 4432 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR, 2, 75)
    c.enemy_group.add(
        frog1, frog2, frog3, frog4, frog5, frog6,
        opossum1, opossum2, opossum3, opossum4, opossum5, opossum6, opossum7
    )
    
    # collectibles
    cherry1 = Collectible('cherry', 1184 * c.SCALE_FACTOR, 176 * c.SCALE_FACTOR)
    cherry2 = Collectible('cherry', 4016 * c.SCALE_FACTOR, 128 * c.SCALE_FACTOR)
    cherry3 = Collectible('cherry', 4288 * c.SCALE_FACTOR, 240 * c.SCALE_FACTOR)
    cherry4 = Collectible('cherry', 4416 * c.SCALE_FACTOR, 128 * c.SCALE_FACTOR)
    cherry5 = Collectible('cherry', 6160 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR)
    cherry6 = Collectible('cherry', 6176 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR)
    cherry7 = Collectible('cherry', 6192 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR)
    cherry8 = Collectible('cherry', 6208 * c.SCALE_FACTOR, 288 * c.SCALE_FACTOR)
    s_cherry1 = Collectible('super_cherry', 2048 * c.SCALE_FACTOR, 176 * c.SCALE_FACTOR)
    s_cherry2 = Collectible('super_cherry', 3008 * c.SCALE_FACTOR, 128 * c.SCALE_FACTOR)
    s_cherry3= Collectible('super_cherry', 5456 * c.SCALE_FACTOR, 192 * c.SCALE_FACTOR)
    c.item_group.add(
        cherry1, cherry2, cherry3, cherry4, cherry5, cherry6, cherry7, cherry8,
        s_cherry1, s_cherry2, s_cherry3
    )
    
    # level and scrolling
    level = Level('levels\level1\\fulldemo.tmx', game.display, player, scale_factor=1.2)
    screen_scroll = 0
    background_scroll = 0
    
    # main loop
    run = True
    while run:
        clock.tick(75)
        game.display.fill((0, 0, 0))
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
                # to draw enemy hitboxes
                # po.draw.rect(game.display, (0, 0, 255), enemy.rect, 3)
                
        # temporary floor
        y_cood = 383
        po.draw.line(game.display, (255, 0, 0), (0, y_cood), (5120, y_cood))

        game.draw(player, player.flip)
        po.draw.rect(game.display, (0, 0, 255), player.rect, 3)
        player.update(game.death_fx)
        
        if player.alive:    
            # retrieve the updated screen scroll values from player.move(), 
            # and also allow player to move 
            screen_scroll = player.move(game, level, background_scroll)

            # for scrolling the background images
            background_scroll -= screen_scroll
            # update player action
            if player.shoot:
                player.shoot(game.shoot_fx, player.isShooting)
            
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