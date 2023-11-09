import pygame as po
import os
import constants as c
import projectiles
from pytmx.util_pygame import load_pygame
from characters import Character
from collectibles import Collectible

po.init()

class Game:
    def __init__(this):
        # actual screen 
        this.height = c.SCREEN_HEIGHT
        this.width = c.SCREEN_WIDTH
        this.screen = po.display.set_mode((this.width, this.height))
        po.display.set_caption('lol')

        # secondary surface, half of main screen, render everything on this
        this.display = po.Surface((this.width * 0.6, this.height * 0.6))
        
        # load level data
        tmx_data = load_pygame('levels\\fulldemo.tmx')
        print(tmx_data.layers)
    
    def draw(this, obj, dir = 1):
        # flip(image, xFlip(true or false), yFlip(True or false))
        # po.draw.rect(this.display, (0, 255, 0), obj.rect, 1)
        this.display.blit(po.transform.flip(obj.image, dir, False), obj.rect)
        this.screen.blit(po.transform.scale(this.display, this.screen.get_size()), (0, 0))
    
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
        po.draw.rect(this.game.display, (0, 0, 0), (this.x - 2, this.y - 2, this.game.width * 0.1, 24))
        po.draw.rect(this.game.display, (255, 0, 0), (this.x, this.y, 35, 5))
        po.draw.rect(this.game.display, (0, 255, 0), (this.x, this.y, 35 * ratio, 5))
    
def main():
    
    # clock for steady fps
    clock = po.time.Clock()
    game = Game()        
    # Character( character_type, x-cood, y-cood, speed, run(True, default = False) )
    player = Character('player', 200, 200, 2, 100, True)
    h_bar = HealthBar(10, 10, player.health, player.max_health, game)
    # frog = Character('frog', 400, 205, 3, 75)
    opossum = Character('opossum', 500, 200, 2, 50)
    c.enemy_group.add(opossum)
    
    # collectibles
    cherry = Collectible('cherry', 300, 110)
    s_cherry = Collectible('super_cherry', 250, 110)
    c.item_group.add(cherry, s_cherry)
    
    # main loop
    run = True
    while run:
        clock.tick(c.FPS)
        game.display.fill((0, 0, 0))
        h_bar.draw(player.health)
        
        # draw and update groups
        for bullet in c.bullet_group:
            game.draw(bullet, bullet.flip)
            bullet.update(player)
            bullet.update(c.enemy_group, True)
        
        for item in c.item_group:
            game.draw(item)
            item.update(player)
        
        for enemy in c.enemy_group:
            e_hBar = HealthBar(enemy.rect.x, enemy.rect.y - 20, enemy.health, enemy.max_health, game)
            e_hBar.draw(enemy.health)
            if player.alive:
                enemy.handle_collision(player)
            if enemy.cType == 'frog':
                enemy.AI(player, game, True)
            else:
                enemy.AI(player, game)
            enemy.update()
            game.draw(enemy, enemy.flip)
            
        # temporary floor
        po.draw.line(game.display, (255, 0, 0), (0, 217), (game.width, 217))

        game.draw(player, player.flip)
        player.update()
        po.draw.rect(game.display, (0, 255, 0), player.rect, 1)
        
        
        if player.alive:    
            player.move()
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
                        player.speed = 3   
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
                        player.speed = 2
                if event.key in (po.K_UP, po.K_w, po.K_z) and player.alive == True:
                    player.jump = False 
                
        po.display.update()
    po.quit()
main()