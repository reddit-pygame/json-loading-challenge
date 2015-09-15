import os
import pygame as pg
import tools


SCREEN_SIZE = (600, 600)
ORIGINAL_CAPTION = "Wolves, Rabbits and Grass"

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
