import pygame as po

class TileTMX(po.sprite.Sprite):
    def __init__(this, pos, surface, groups):
        super().__init__(groups)
        this.image = surface
        this.rect = this.image.get_rect(topleft = pos)
        this.collidable_tiles = 'platforms'
        this.original_rect = this.rect.copy()
        
        # this.rect.width = int(this.original_rect.width * c.SCALE_FACTOR)
        # this.rect.height = int(this.original_rect.height * c.SCALE_FACTOR)
        # this.rect.topleft = (
        #     int(this.original_rect.topleft[0] * c.SCALE_FACTOR),
        #     int(this.original_rect.topleft[1] * c.SCALE_FACTOR)
        # )
    def update(this, x_offset):
        this.rect.x += x_offset
        
        # # Update the rect based on the current scale_factor
        # this.rect.width = int(this.original_rect.width * c.SCALE_FACTOR)
        # this.rect.height = int(this.original_rect.height * c.SCALE_FACTOR)
        # this.rect.topleft = (
        #     int(this.original_rect.topleft[0] * c.SCALE_FACTOR),
        #     int(this.original_rect.topleft[1] * c.SCALE_FACTOR)
        # )

