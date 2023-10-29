<<<<<<< HEAD
import pygame as po

# game variables
FPS = 80
GRAVITY = 0.3
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900 
TILE_SIZE = 40

# player action variables
CHAR_IDLE = 0
CHAR_JUMP = 1
CHAR_DEATH = 2
CHAR_RUN = 3
CHAR_CROUCH = 4
CHAR_CLIMB = 5
CHAR_HURT = 6

# groups
enemy_group = po.sprite.Group()
item_group = po.sprite.Group()
=======
import pygame as po

# game variables
FPS = 80
GRAVITY = 0.3
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900 
TILE_SIZE = 40

# player action variables
CHAR_IDLE = 0
CHAR_JUMP = 1
CHAR_DEATH = 2
CHAR_RUN = 3
CHAR_CROUCH = 4
CHAR_CLIMB = 5
CHAR_HURT = 6

# groups
enemy_group = po.sprite.Group()
item_group = po.sprite.Group()
>>>>>>> 74dd59ebbee89e33b3e48475a4d4ddbe2697e028
bullet_group = po.sprite.Group()