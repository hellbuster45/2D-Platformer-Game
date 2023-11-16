import pygame as po
import os
import game_data as c

class Collectible(po.sprite.Sprite):
    def __init__(this, itype, x, y):
        po.sprite.Sprite.__init__(this)
        this.item_type = itype

        # Specify the path to the directory you want to access
        directory_path = "assets\Sunny-land-files\Graphical Assets\sprites\\" + this.item_type

        # will be used whenever a collectible item will have multiple states ( which is unlikely, atleast right now )
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
        this.item_sprites = []
        this.update_time = po.time.get_ticks()
        this.frame_index = 0
        this.action = 0

        for animation in animation_types:
            # reset list
            temp_list = []
            
            # count number of sprites
            num_of_sprites = len(os.listdir(f'assets\Sunny-land-files\Graphical Assets\sprites\{this.item_type}\{animation}'))

            for i in range(num_of_sprites):
                this.image = po.image.load(f'assets\Sunny-land-files\Graphical Assets\sprites\{this.item_type}\{animation}\{animation}-{ i + 1 }.png').convert_alpha()
                if this.item_type == 'super_cherry':
                    temp_list.append(po.transform.scale(this.image, (1.5 * this.image.get_width(), 1.5 * this.image.get_height())))
                else:
                    temp_list.append(this.image)
            this.item_sprites.append(temp_list)
        this.image = this.item_sprites[this.action][this.frame_index] 

        # image rectangle for collisions n stuff
        this.rect = this.image.get_rect()
        this.rect.midtop = (x + c.TILE_SIZE // 2, y + (c.TILE_SIZE - this.image.get_height()))

    def update(this, char, screen_scroll, item_fx):
        
        # scroll the collectibles along with the screen too
        this.rect.x += screen_scroll
        
        this.update_animation()
        if po.sprite.collide_rect(this, char):
                if char.alive:
                    # update health based on type of cherries
                    if this.item_type == 'super_cherry' and this.action != 1:
                        item_fx.play()
                        char.health += 50
                        this.update_action(1)
                    if this.item_type == 'cherry'and this.action != 1:
                        item_fx.play()
                        char.health += 25
                        this.update_action(1)
                    # limit health at 100    
                    if char.health > char.max_health:
                        char.health = char.max_health

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
        this.image = this.item_sprites[this.action][this.frame_index]

        # this is something :/, dunno how this works yet
        if po.time.get_ticks() - this.update_time > ANIMATION_COOLDOWN:
            this.update_time = po.time.get_ticks()
            this.frame_index += 1

        # check if index has gone beyond animation_list's length ( looping animation basically )
        if this.frame_index >= len(this.item_sprites[this.action]):
            if this.action == 1:
                this.frame_index = -1
                this.action = 0
                this.kill()
            else:
                this.frame_index = 0