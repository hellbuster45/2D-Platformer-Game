import pygame as po
from pytmx.util_pygame import load_pygame
import game_data as c

class TileTMX(po.sprite.Sprite):
    def __init__(this, pos, surface, groups):
        super().__init__(groups)
        this.image = surface
        this.rect = this.image.get_rect(topleft = pos)
        this.collidable_tiles = 'platforms'
        
    def update(this, x_offset):
        this.rect.x += x_offset

