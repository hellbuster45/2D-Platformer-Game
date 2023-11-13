import pygame as po
import game_data as c
from pytmx.util_pygame import load_pygame
from characters import Character
from collectibles import Collectible
from level import Level

po.init()

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
        this.mid_front = po.image.load('levels\level1\\background_PNGs\mid_front.png').convert_alpha()
        this.mid_back = po.image.load('levels\level1\\background_PNGs\mid_back.png').convert_alpha()
        this.s_width = this.sky.get_width()
        this.mf_width = this.mid_front.get_width()
        this.mb_width = this.mid_back.get_width()
        this.props = po.image.load('levels\level1\\background_PNGs\props.png').convert_alpha()
        this.caves_background = po.image.load('levels\level1\\background_PNGs\caves_background.png').convert_alpha()

    def draw(this, obj, dir = 1):
        this.display.blit(po.transform.flip(obj.image, dir, False), obj.rect)
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

# left for ujjwal :P    
class MainMenu:
    def __init__(this):
        pass
    

class HealthBar(Game):
    def __init__(this, x, y, health, max_health, game):
        this.x = x
        this.y = y
        this.game = game
        this.health = health
        this.max_health = max_health
    
    def draw(this, health):
        # update health for the health bar
        this.health = health
            
        # calculate ratio for health
        ratio = this.health / this.max_health
            
        # draw the health bar based on the ratio
        po.draw.rect(this.game.display, (0, 0, 0), (this.x - 2, this.y - 2, 54, 14))
        po.draw.rect(this.game.display, (255, 0, 0), (this.x, this.y, 50, 10))
        po.draw.rect(this.game.display, (0, 255, 0), (this.x, this.y, 50 * ratio, 10))
   
def main():
    # clock for steady fps
    clock = po.time.Clock()
    game = Game()      
      
    # Character( character_type, x-cood, y-cood, speed)
    player = Character('player', 90, 200, 3, 100)
    h_bar = HealthBar(10, 10, player.health, player.max_health, game)
    frog = Character('frog', 1380, 200, 3, 100)
    opossum = Character('opossum', 500, 200, 2, 75)
    c.enemy_group.add(frog, opossum)
    
    # collectibles
    cherry = Collectible('cherry', 300, 110)
    s_cherry = Collectible('super_cherry', 250, 110)
    c.item_group.add(cherry, s_cherry)
    
    # level and scrolling
    level = Level('levels\level1\\fulldemo.tmx', game.display, player, scale_factor=1.2)
    screen_scroll = 0
    background_scroll = 0
    
    # main loop
    run = True
    while run:
        clock.tick(c.FPS)
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
                item.update(player, screen_scroll)
            
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
        # y_cood = 200
        # po.draw.line(game.display, (255, 0, 0), (0, y_cood), (5120, y_cood))

        game.draw(player, player.flip)
        po.draw.rect(game.display, (0, 0, 255), player.rect, 3)
        player.update()
        
        if player.alive:    
            # retrieve the updated screen scroll values from player.move(), 
            # and also allow player to move 
            screen_scroll = player.move(game, level, background_scroll)
            
            # for scrolling the background images
            background_scroll -= screen_scroll
            # update player action
            if player.shoot:
                player.shoot(player.isShooting)
            
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