import pygame as po
import pytmx
import game_data as c
from TilesTMX import TileTMX

def load_map(tmx_data):
    sprite_group = po.sprite.Group()
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surface in layer.tiles():
                pos = (x * 16, y * 16)
                TileTMX(pos = pos, surface = surface, groups = sprite_group)
    return sprite_group

class Level:
    def __init__(this, path, surface, player, scale_factor):
        this.player = player
        this.surface = surface
        this.world_shift = 0

        # Load TMX file
        tmx_data = pytmx.load_pygame(path)
        this.layer_sprites = load_map(tmx_data)
        this.level_width = tmx_data.width * tmx_data.tilewidth
        this.level_height = tmx_data.height * tmx_data.tileheight

    def draw(this):
        
        for tile in this.layer_sprites.sprites():
            # if (tile.rect.x <= 0 + c.TILE_SIZE and tile.rect.x >= 0 - c.TILE_SIZE) or (tile.rect.x < c.SCREEN_WIDTH + c.TILE_SIZE and tile.rect.x > c.SCREEN_WIDTH - c.TILE_SIZE):
            if tile.rect.left < c.SCREEN_WIDTH and tile.rect.right > 0:
                this.surface.blit(tile.image, tile.rect)

    def run(this, alive, screen_scroll):
        if alive == True:
            this.layer_sprites.update(screen_scroll)
        this.draw()