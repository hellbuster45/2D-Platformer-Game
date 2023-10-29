import pygame as po
import os
import constants as c
# items = {
#     cherry : for sprite in 
# }

class Collectible(po.sprite.Sprite):
    def __init__(this, itype, x, y):
        po.sprite.Sprite.__init__(this)
        this.item_type = itype
        
        # Specify the path to the directory you want to access
        directory_path = "python-game\\assets\Sunny-land-files\Graphical Assets\sprites\\" + this.item_type

        # # Initialize an empty list to store folder names
        # animation_types = []

        # # Check if the directory exists
        # if os.path.exists(directory_path) and os.path.isdir(directory_path):
        #     # List all items (files and folders) in the specified directory
        #     items = os.listdir(directory_path)

        #     # Filter out only the folders
        #     for item in items:
        #         item_path = os.path.join(directory_path, item)
        #         if os.path.isdir(item_path):
        #             animation_types.append(item)
        
        # storing all sprites in animation_list[]     
        this.item_sprites = []
        this.update_time = po.time.get_ticks()
        this.frame_index = 0
        this.action = 0
        
        # count number of sprites
        num_of_sprites = len(os.listdir(f'python-game\\assets\Sunny-land-files\Graphical Assets\sprites\{this.item_type}'))
        
        for i in range(num_of_sprites):
            this.image = po.image.load(f'python-game\\assets\Sunny-land-files\Graphical Assets\sprites\{this.item_type}\{this.item_type}-{ i + 1 }.png').convert_alpha()
            if this.item_type == 'super_cherry':
                this.item_sprites.append(po.transform.scale(this.image, (1.5 * this.image.get_width(), 1.5 * this.image.get_height())))
            else:
                this.item_sprites.append(this.image)        
        this.items = {}
        this.items.update({f'{this.item_type}' : this.item_sprites})
        this.image = this.items[this.item_type][0]  
        
        # image rectangle for collisions n stuff
        this.rect = this.image.get_rect()
        this.rect.midtop = (x + c.TILE_SIZE // 2, y + (c.TILE_SIZE - this.image.get_height()))
        
    def update(this, char):
        this.update_animation()
        if po.sprite.collide_rect(this, char):
                if char.alive:
                    print(f'{char.cType}, {char.health}')
                    
                    # update health based on type of cherries
                    if this.item_type == 'super_cherry':
                        char.health += 40
                    else:
                        char.health += 20
                        
                    # limit health at 100    
                    if char.health > char.max_health:
                        char.health = char.max_health
                    print(f'{char.cType}, {char.health}')
                    
                    this.kill()
    
    def update_animation(this): 
        
        # frame time
        ANIMATION_COOLDOWN = 110
        
        # update image with current frame
        this.image = this.items[this.item_type][this.frame_index]
        
        # this is something :/, dunno how this works yet
        if po.time.get_ticks() - this.update_time > ANIMATION_COOLDOWN:
            this.update_time = po.time.get_ticks()
            this.frame_index += 1
        
        # check if index has gone beyond animation_list's length ( looping animation basically )
        if this.frame_index >= len(this.items[this.item_type]):
            this.frame_index = 0