import pygame as po
import os
import constants as c

class Bullet(po.sprite.Sprite):
    def __init__(this, x, y, direction):
        po.sprite.Sprite.__init__(this)
        this.speed = 5
        
        this.bullet_img = []
        bullet_scale = 0.3
        
        # if i want only one bullet sprite
        img = po.image.load(f'python-game\\assets\\bullet sprites\Laser Sprites\\3.png').convert_alpha()
        this.image = po.transform.scale(img, (int(img.get_width() * bullet_scale), int(img.get_height() * bullet_scale)))
        # if i want multiple bullet sprites
        # for i in range(1, 4):
        #     bullet_img = po.image.load(f'bullet sprites\Laser Sprites\{i}.png').convert_alpha()
            
        #     # Scale the bullet image
        #     this.image = po.transform.scale(bullet_img, (int(bullet_img.get_width() * bullet_scale), int(bullet_img.get_height() * bullet_scale)))
        #     this.bullet_img.append(this.image)
        # this.image = this.bullet_img[0]
        this.rect = this.image.get_rect()
        this.rect.center = (x, y)
        this.direction = direction
        this.frame_index = 0
        if this.direction == -1:
            this.flip = True
        else:
            this.flip = False

    def update(this, char, group = False):
        # this.frame_index = (this.frame_index + 1) % len(this.bullet_img)
        # this.image = this.bullet_img[this.frame_index]
        
        # Update the bullet's position based on its speed and direction
        this.rect.x += this.speed * this.direction
        
        # delete bullet as soon as it goes off-screen
        if this.rect.right < 0 or this.rect.left > c.SCREEN_WIDTH * 0.6:
            this.kill()
        
        if group:
            for ch in char:
                if po.sprite.spritecollide(ch, c.bullet_group, 0):
                    if ch.alive:
                        ch.health -= 10
                        this.kill()
        else:
            if po.sprite.spritecollide(char, c.bullet_group, 0):
                if char.alive:
                    char.health -= 10
                    print(f'char: {char.cType}, Health: {char.health}')
                    this.kill()