import pygame as pg

# define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
TILESIZE = 64
WIDTH = TILESIZE*16  # multiple of TILESIZE
HEIGHT = TILESIZE*10  # multiple of TILESIZE
FPS = 60
TITLE = 'Tilemap Demo'
BGCOLOR = DARKGREY

GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# Player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
