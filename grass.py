import pygame as pg
from prepare import GFX


class Grass(pg.sprite.DirtySprite):
    images = {x: GFX["grass{}".format(x)] for x in range(5)}
    
    def __init__(self, pos, growth, *groups):
        super(Grass, self).__init__(*groups)
        self.pos = pos
        self.growth = growth
        self.max_growth = 1000
        self.turn_chance = 3
        self.image = self.images[4]
        self.set_image()
        self.rect = self.image.get_rect(center=pos)        
        
    def set_image(self):
        old_image = self.image
        num = min(4, self.growth // (self.max_growth//5))
        self.image = self.images[num]
        self.rect = self.image.get_rect(center=self.pos)
        if self.image != old_image:
            self.dirty = 1

    def update(self, dt):
        self.growth = min(self.growth + 1, self.max_growth)
        self.set_image()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)