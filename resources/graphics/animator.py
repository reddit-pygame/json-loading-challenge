import sys
from itertools import cycle
import pygame as pg


class Animator(object):
    def __init__(self):
        self.screen = pg.display.set_mode((800, 800))
        self.clock = pg.time.Clock()
        self.fps = 60
        images = [pg.image.load("foxleft{}.png".format(i)).convert_alpha() for i in (1,2,3,4,5)]
        #images = [pg.image.load("bat{}.png".format(i)).convert_alpha() for i in (1,2)]
        flipped_images = [pg.transform.flip(img, True, False) for img in images]
        self.images = cycle(flipped_images)
        self.image = next(self.images)
        self.anim_time = 140
        self.anim_timer = 0.0
        self.done = False
        
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                elif event.key == pg.K_UP:
                    self.anim_time += 1
                    print "Anim Time: {}".format(self.anim_time)
                elif event.key == pg.K_DOWN:
                    self.anim_time -= 1
                    print "Anim Time: {}".format(self.anim_time)                    
                
    def update(self, dt):
        self.anim_timer += dt
        while self.anim_timer >= self.anim_time:
            self.anim_timer -= self.anim_time
            self.image = next(self.images)
        
    def draw(self, surface):
        surface.fill(pg.Color("red"))
        surface.blit(self.image, (0, 0))
        
    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw(self.screen)
            pg.display.update()
            
            
if __name__ == "__main__":
    animator =Animator()
    animator.run()
    pg.quit()
    sys.exit()