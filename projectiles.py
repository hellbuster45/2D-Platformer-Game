import pygame as po
import os
import game_data as c

class Bullet(po.sprite.Sprite):
    def __init__(this, x, y, direction):
        po.sprite.Sprite.__init__(this)
        this.speed = 10
        
        this.bullet_img = []
        bullet_scale = 0.4
        
        # if i want only one bullet sprite
        img = po.image.load(f'assets\\bullet sprites\Laser Sprites\\3.png').convert_alpha()
        this.image = po.transform.scale(img, (int(img.get_width() * bullet_scale), int(img.get_height() * bullet_scale)))
        this.rect = this.image.get_rect()
        this.rect.center = (x, y)
        this.direction = direction
        this.frame_index = 0
        if this.direction == -1:
            this.flip = True
        else:
            this.flip = False

    def update(this, char, level, screen_scroll, group = False):
        # Update the bullet's position based on its speed and direction
        this.rect.x += this.speed * this.direction
        
        # scroll the projectiles along with the screen too 
        this.rect.x += screen_scroll
        
        # delete bullet as soon as it goes off-screen
        if this.rect.right < 0 or this.rect.left > c.SCREEN_WIDTH:
            this.kill()
            
        for tile in level.layer_sprites.sprites():
            if tile.rect.colliderect(this.rect):
                this.kill()
        if group:
            for ch in char:
                speed = ch.speed
                if po.sprite.spritecollide(ch, c.bullet_group, 0):
                    if ch.alive:
                        ch.health -= 20
                        ch.speed = 0
                        this.kill()
                        ch.speed = speed
        else:
            pass
            # # bullet hits player
            # if po.sprite.spritecollide(char, c.bullet_group, 0):
            #     if char.alive:
            #         char.health -= 25
            #         print(f'char: {char.cType}, Health: {char.health}')
            #         this.kill()