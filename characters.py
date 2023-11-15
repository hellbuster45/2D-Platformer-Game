import pygame as po
import os
import random as r
import game_data as c
from projectiles import Bullet
from level import Level

class Character(po.sprite.Sprite):
    def __init__(this, type, x, y, speed, health):
        po.sprite.Sprite.__init__(this)
        
        # no explanation needed beruh -_-
        this.death_fx = po.mixer.Sound('sfx\death.wav')
        this.death_fx.set_volume(0.03)
        this.hitHurt_fx = po.mixer.Sound('sfx\hitHurt.wav')
        this.hitHurt_fx.set_volume(0.05)
        this.alive = True
        this.health = health
        this.max_health = this.health
        this.invincible = False
        this.invincible_counter = 0
        this.cType = type
        
        # speed n direction duh!
        this.speed = speed
        this.direction = 1
        this.flip = False
        
        # movement
        this.move_left = False
        this.move_right = False
        
        # jump
        this.jump = False
        this.y_velocity = 0
        this.inAir = True
        this.inAir_counter = 0
        this.isUp = False
        this.isDown = False
        
        # shoot
        this.isShooting = False
        this.shootCooldown = 0

        # Specify the path to the directory you want to access
        directory_path = "assets\Sunny-land-files\Graphical Assets\sprites\\" + this.cType

        # Initialize an empty list to store folder names
        animation_types = []

        # Check if the directory exists
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            # List all items (files and folders) in the specified directory
            items = os.listdir(directory_path)
            
            # Filter out only the folders
            for item in items:
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    animation_types.append(item)
        # storing all sprites in animation_list[]     
        this.animation_list = []
        this.update_time = po.time.get_ticks()
        this.frame_index = 0
        this.action = 0
        
        for animation in animation_types:
            # reset list
            temp_list = []
            
            # count number of sprites
            num_of_sprites = len(os.listdir(f'assets\Sunny-land-files\Graphical Assets\sprites\{this.cType}\{animation}'))
            
            for i in range(num_of_sprites):
                this.image = po.image.load(f'assets\Sunny-land-files\Graphical Assets\sprites\{this.cType}\{animation}\{animation}-{ i + 1 }.png').convert_alpha()
                temp_list.append(this.image)
            this.animation_list.append(temp_list)
        this.image = this.animation_list[this.action][this.frame_index]            
        
        # image rectangle for collisions n stuff
        this.rect = this.image.get_rect()
        this.rect.center = (x, y)
        this.width = this.image.get_width()
        this.height = this.image.get_height()
        
        # AI variables
        this.move_counter = 0
        this.idle = False
        this.idle_counter = 50
        this.vision = po.Rect(0, 0, 250, 10)
      
    def move(this, game, level, bg_scroll):
        # Reset movement
        dx = 0
        dy = 0
        screen_scroll = 0
        
        # movement
        if this.move_left:
            dx = -this.speed
            
            # sets the direction to flip the sprites accordingly in Game.draw()
            this.direction = -1
            this.flip = True
            
        if this.move_right:
            dx = this.speed
            
            # sets the direction to flip the sprites accordingly in Game.draw()
            this.direction = 1
            this.flip = False

        # jumping
        if this.jump and this.inAir == False:
            if this.cType == 'frog':
                this.y_velocity = -3
                this.inAir_counter = 5
                this.isUp = True
            else:
                game.jump_fx.play()
                this.y_velocity = -7
                this.inAir_counter = 21
                this.isUp = True
            this.jump = False
            this.inAir = True
        if this.inAir:
            this.inAir_counter -= 1
            if this.inAir_counter <= 0:
                this.isDown = True
                this.isUp = False
        this.y_velocity += c.GRAVITY
        dy += this.y_velocity
        
        if this.y_velocity > 15:
            this.y_velocity = 0
        
        # actual collision with the level tiles
        for tile in level.layer_sprites.sprites():
            # if tile.collidable_tiles == 'platforms':
            if tile.rect.colliderect(this.rect.x, this.rect.y + dy, this.width, this.height):
                # If player is jumping inot a tile, bumping it's head
                if this.y_velocity < 0:
                    this.y_velocity = 0
                    # allow to player to only move the distance of the gap between the tile's bottom and the player's head
                    dy = tile.rect.bottom - this.rect.top
                elif this.y_velocity >= 0:
                    this.y_velocity = 0
                    # allow the player to only fall the distance of the gap between the tile's top and the player's feet
                    dy = tile.rect.top - this.rect.bottom
                    this.inAir = False
                    this.isUp = False
                    this.isDown = False
                    if this.cType == 'frog':
                        this.idle = True
                        this.idle_counter = r.randint(50, 60)
                        this.update_action(c.CHAR_IDLE)
            
            # Horizontal collision
            if tile.rect.colliderect(this.rect.x + dx, this.rect.y, this.width, this.height):
                if tile.rect.y > this.rect.y:
                    dx = 0
                else:
                    if this.cType == 'frog' or this.cType == 'opossum':
                        this.direction *= -1
                        this.move_counter = 0
                  
        # check if player is going off boundaries
        if this.cType == 'player':
            if this.rect.left + dx < 0 or this.rect.right + dx > c.SCREEN_WIDTH:
                dx = 0
            elif this.rect.left + dx < 0 or this.rect.right + dx > level.level_width:
                dx = 0
        
        # Update player's position with floats
        this.rect.x += float(dx)
        this.rect.y += float(dy)

        # when a character goes beyond this y value, kill it
        if this.rect.bottom >= 447:
            this.health -= 200
        
        # update screen scrolling
        if this.cType == 'player':
            if (this.rect.right > c.SCREEN_WIDTH - (2 * c.SCROLL_THRESHHOLD) and bg_scroll < ((level.level_width) - c.SCREEN_WIDTH)) or (this.rect.left < c.SCROLL_THRESHHOLD and bg_scroll > abs(dx)):
                if this.rect.right < level.level_width:
                   
                   # dx tells us how much the player will move, 
                   # when the threshhold is reached, we negate the dx value added to the player, in order to not allow him to move
                   this.rect.x -= dx
                   
                   # instead we move the screen to the opposite direction,
                   # by the amount the player was gonna move ( dx )
                   screen_scroll = -dx 
        
        return screen_scroll
        
    def shoot(this, shoot_fx, image, isShooting):
        if this.isShooting and this.shootCooldown == 0:
            this.shootCooldown = 4
            
            # spawn a bullet, this.rect.size[0] gives the width of the character sprite
            bullet = Bullet(this.rect.centerx + (0.75 * this.rect.size[0] * this.direction), this.rect.centery, image, this.direction)
            c.bullet_group.add(bullet)
            shoot_fx.play()
    
    def AI(this, player, game, level, screen_scroll, bg_scroll, frog = False):
        
        if this.alive and player.alive:
            
            # when enemy is not idle and 4 gets generated randomly, set enemy to idle and idle counter to 50 
            if this.idle == False and r.randint(1, 200) == 4 and frog == False and this.vision.colliderect(player.rect) == False:
                this.idle = True
                this.idle_counter = 50

            # if enemy is not idle, implement movement    
            if this.idle == False:
                
                #basic movement
                if this.direction == 1:
                    this.move_right = True
                else:
                    this.move_right = False
                this.move_left = not this.move_right
                this.move(game, level, bg_scroll) 
                
                # update enemy vision rectangle along with movement
                this.vision.center = (this.rect.centerx + 125 * this.direction, this.rect.centery)
                po.draw.rect(game.display, (255, 0, 0), this.vision)
                
                # frog jump movement
                if frog:
                    if this.idle:
                        this.update_action(c.CHAR_IDLE)
                    else:    
                        this.update_action(c.CHAR_JUMP)
                    this.jump = True   
                else:
                    this.update_action(c.CHAR_RUN)   
                
                # if enemy has player in vision, follow it, else, keep patrolling
                if this.vision.colliderect(player.rect):
                    this.idle = False
                    this.idle_counter = 0
                    if player.move_left:
                        # this.dierection = -1
                        this.move_left = True
                    elif player.move_right:
                        # this.dierection = 1
                        this.move_right = True    
                else:    
                    this.move_counter += 1
                    if this.move_counter > (2 * c.TILE_SIZE):
                        this.direction *= -1
                        this.move_counter *= -1
            else:
                # if enemy is idle, decrement the idle counter, when it reaches 0, set enemy to not idle anymore
                this.idle_counter -= 1
                if this.idle_counter <= 0:
                    this.idle = False
            
            # scroll the enemies along with the screen too..
            this.rect.x += screen_scroll
        
    def handle_collision(this, level, player):
        if player.invincible == False:
            if po.sprite.collide_rect(this, player):
                player.hitHurt_fx.play()
                player.health -= 50
                player.invincible = True
                player.invincible_counter = 100

                # calculate knockback direction
                knockback_dir = player.rect.centerx - this.rect.centerx
                # normalize to -1 or 1
                if knockback_dir < 0:
                    knockback_dir = -1
                else:
                    knockback_dir = 1

                # apply knockback
                player.rect.x += knockback_dir * c.KNOCKBACK_FORCE
                
                # # reset jump variables
                player.isUp = False
                player.isDown = False
        else:
            player.invincible_counter -= 1
            if player.invincible_counter <= 0:
                player.invincible = False
        
    def update(this, ):
        this.update_animation()
        this.check_alive()
        # update cooldown    
        if this.shootCooldown > 0:
            this.shootCooldown -= 1
    
    def check_alive(this):
        if this.health <= 0:
            this.health = 0
            this.speed = 0
            this.alive = False
            if this.death_fx != None:
                this.death_fx.play(0)
            this.death_fx = None
            this.update_action(c.CHAR_DEATH)

    def update_action(this, new_action):
        
        if new_action != this.action:
            this.action = new_action
            this.frame_index = 0    
            
            # again no idea, how this works :/
            this.update_time = po.time.get_ticks()

    def update_animation(this): 
        # frame time
        ANIMATION_COOLDOWN = 100
            
        # update image with current frame
        if (this.cType == 'player' or this.cType == 'frog') and this.alive == True:
            if this.isUp == True and this.isDown == False:
                this.image = this.animation_list[c.CHAR_JUMP][0]
            elif this.isDown == True and this.isUp == False:
                this.image = this.animation_list[c.CHAR_JUMP][1]
            else:
                this.image = this.animation_list[this.action][this.frame_index]
        else:
            this.image = this.animation_list[this.action][this.frame_index]
            
        # this is something :/, dunno how this works yet
        if po.time.get_ticks() - this.update_time > ANIMATION_COOLDOWN:
            this.update_time = po.time.get_ticks()
            this.frame_index += 1

        # check if index has gone beyond animation_list's length ( looping animation basically )
        if this.frame_index >= len(this.animation_list[this.action]):
            if this.action == c.CHAR_DEATH:
                this.frame_index = len(this.animation_list[this.action]) - 1
                this.kill()
            else:
                this.frame_index = 0