import pygame as po

class TileTMX(po.sprite.Sprite):
    def __init__(this, pos, surface, groups):
        super().__init__(groups)
        this.image = surface
        this.rect = this.image.get_rect(topleft = pos)
        this.collidable_tiles = 'platforms'
        this.original_rect = this.rect.copy()
        
    def update(this, x_offset):
        this.rect.x += x_offset