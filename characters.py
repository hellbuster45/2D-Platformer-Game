import pygame as po
import os
import constants as c
from projectiles import Bullet

class Character(po.sprite.Sprite):
    def __init__(this, type, x, y, speed, health, run = False):
        po.sprite.Sprite.__init__(this)
        
        # no explanation needed beruh -_-
        this.alive = True
        this.health = health
        this.max_health = this.health
        
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
        
        # shoot
        this.isShooting = False
        this.shootCooldown = 0

        # Specify the path to the directory you want to access
        directory_path = "python-game\\assets\Sunny-land-files\Graphical Assets\sprites\\" + this.cType

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
            num_of_sprites = len(os.listdir(f'python-game\\assets\Sunny-land-files\Graphical Assets\sprites\{this.cType}\{animation}'))
            
            for i in range(num_of_sprites):
                this.image = po.image.load(f'python-game\\assets\Sunny-land-files\Graphical Assets\sprites\{this.cType}\{animation}\{animation}-{ i + 1 }.png').convert_alpha()
                temp_list.append(this.image)
            this.animation_list.append(temp_list)
        this.image = this.animation_list[this.action][this.frame_index]            
        
        # image rectangle for collisions n stuff
        this.rect = this.image.get_rect()
        this.rect.center = (x, y)
      
    def move(this):
        # Reset movement
        dx = 0
        dy = 0

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
            this.y_velocity = -7
            this.jump = False
            this.inAir = True
        this.y_velocity += c.GRAVITY
        dy += this.y_velocity
        
        # temporary floor collision
        if this.rect.bottom + dy > 217:
            dy = 217 - this.rect.bottom
            this.inAir = False
        
        # Update player's position with floats
        this.rect.x += float(dx)
        this.rect.y += float(dy)
        
        
    def shoot(this, isShooting):
        if this.isShooting and this.shootCooldown == 0:
            this.shootCooldown = 15
            # spawn a bullet, this.rect.size[0] gives the width of the character sprite
            bullet = Bullet(this.rect.centerx + (0.75 * this.rect.size[0] * this.direction), this.rect.centery, this.direction)
            c.bullet_group.add(bullet)
    
    def AI(this):
        pass
            
    def update(this):
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
            this.update_action(c.CHAR_DEATH)

    def update_action(this, new_action):
        
        if new_action != this.action:
            this.action = new_action
            this.frame_index = 0    
            
            # again no idea, how this works :/
            this.update_time = po.time.get_ticks()
            
    def update_animation(this): 
        
        # frame time
        ANIMATION_COOLDOWN = 110
        
        # update image with current frame
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