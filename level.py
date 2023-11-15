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
            # # Scale the image
            # scaled_image = po.transform.scale(tile.image, (int(tile.rect.width * c.SCALE_FACTOR), int(tile.rect.height * c.SCALE_FACTOR)))

            # # Scale and draw the tile
            # # scaled_rect = po.Rect(tile.rect.x * c.SCALE_FACTOR, tile.rect.y * c.SCALE_FACTOR, tile.rect.width * c.SCALE_FACTOR, tile.rect.height * c.SCALE_FACTOR)
            # this.surface.blit(scaled_image, tile.rect)
            
            # # draw tile hitboxes
            # # po.draw.rect(this.surface, (0, 255, 0), tile.rect, 1)

    def run(this, alive, screen_scroll):
        if alive == True:
            this.layer_sprites.update(screen_scroll)
        this.draw()