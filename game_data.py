from pygame import sprite
# game variables
FPS = 75
GRAVITY = 0.3
TILE_TYPES = 91
TILE_SIZE = 16
ROWS = 29
COLUMNS = 400
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = TILE_SIZE * ROWS
SCROLL_THRESHHOLD = 200
LEVEL = 1
KNOCKBACK_FORCE = TILE_SIZE * 5

# player action variables
CHAR_IDLE = 0
CHAR_JUMP = 1
CHAR_DEATH = 2
CHAR_RUN = 3
CHAR_CROUCH = 4
CHAR_CLIMB = 5
CHAR_HURT = 6

# groups
enemy_group = sprite.Group()
item_group = sprite.Group()
bullet_group = sprite.Group()