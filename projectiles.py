import pygame as po
import game_data as c

class Bullet(po.sprite.Sprite):
    def __init__(this, x, y, image, direction):
        po.sprite.Sprite.__init__(this)
        this.speed = 25
        this.bullet_img = []
        
        # if i want only one bullet sprite
        img = po.image.load(f'assets\\bullet sprites\Laser Sprites\\3.png').convert_alpha()
        this.image = image
        this.width = this.image.get_width()
        this.height = this.image.get_height()
        this.rect = this.image.get_rect()
        this.rect.center = (x, y)
        this.frame_index = 0
        
        this.direction = direction
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
            # Horizontal collision
            if tile.rect.colliderect(this.rect.x, this.rect.y, this.width, this.height):
                this.kill()
        
        if group:
            for ch in char:
                speed = ch.speed
                if po.sprite.spritecollide(ch, c.bullet_group, 0):
                    if ch.alive:
                        ch.health -= 8
                        ch.speed = 0
                        this.kill()
                        ch.speed = speed