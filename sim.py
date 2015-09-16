from random import randint, choice
import itertools as it
import json
import pygame as pg

import tools, prepare
from state_engine import GameState
from critter import Rabbit, Wolf
from grass import Grass


def random_pos(rect):
    return (randint(rect.left, rect.right), 
                randint(rect.top, rect.bottom))


class Sim(GameState):
    """The main state of the game."""
    def __init__(self):
        super(Sim, self).__init__()
        self.screen_rect = prepare.SCREEN.get_rect()
        self.spawn_rect = self.screen_rect.inflate(-64, -64)
        self.background = pg.Surface(self.screen_rect.size)
        self.background.fill(pg.Color(134, 173, 76))
        self.frame_time = 15
        self.min_rabbits = 1
        self.min_wolves = 0
        
    def startup(self, persistent):
        """
        Activate the state and take in grass, rabbit and
        wolf populations from Menu Screen.
        """
        self.timer = 0
        self.persist = persistent    
        self.grasses = self.persist["grasses"]
        self.rabbits = self.persist["rabbits"]
        self.wolves = self.persist["wolves"]
        self.all_sprites = pg.sprite.LayeredDirty(self.grasses, 
                                                                self.rabbits, self.wolves)
        self.all_sprites.clear(prepare.SCREEN, self.background)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
            self.save()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.frame_time = max(5, self.frame_time - 1)
            elif event.key == pg.K_DOWN:
                self.frame_time += 1
            
    def update(self, dt):
        directions = ("left", "right", "up", "down")
        self.timer += dt
        ft = self.frame_time
        while self.timer >= ft:
            self.timer -= ft
            self.grasses.update(ft)
            self.rabbits.update(ft, self.grasses)
            self.wolves.update(ft, self.rabbits)
            
            for rabbit in self.rabbits:
                if (not rabbit.eating and 
                        rabbit.fertility > rabbit.gestation_period and
                        rabbit.food > rabbit.max_food // 2 and
                        randint(0, 1000) <= rabbit.reproduction_chance):
                    Rabbit(rabbit.pos, choice(directions), 1000, 0,
                              self.rabbits, self.all_sprites)
                    rabbit.fertility = 0
            for wolf in self.wolves:
                if (wolf.fertility > wolf.gestation_period and
                        randint(0, 1000) < wolf.reproduction_chance):
                    Wolf(wolf.pos, choice(directions), 1000, 0,
                            self.wolves, self.all_sprites)
                    wolf.fertility = 0          
        
        if len(self.wolves) < self.min_wolves:
            Wolf(random_pos(self.spawn_rect), choice(directions), 1000, 0,
                    self.wolves, self.all_sprites)
        if len(self.rabbits) < self.min_rabbits:
            Rabbit(random_pos(self.spawn_rect), choice(directions), 1000, 0,
                      self.rabbits, self.all_sprites)
        for s in self.all_sprites:
            self.all_sprites.change_layer(s, s.rect.bottom) 
                
    def draw(self, surface):
        """
        Draw the current state and return dirty rect list to
        be passed to pg.display.update.
        """
        return self.all_sprites.draw(surface)
               
    def save(self):
        """
        Save the current state of all grasses, rabbits and wolves
        as a JSON dict and write to file.
        """
        saved = {}
        saved["rabbits"] = [[r.pos, r.direction, r.food, r.age] for r in self.rabbits]
        saved["grass"] = [[g.pos, g.growth] for g in self.grasses]
        saved["wolves"] = [[w.pos, w.direction, w.food, w.age] for w in self.wolves]
        with open("save.json", "w") as save_file:
            json.dump(saved, save_file)
        
    def run(self):
        """Run the simulation."""
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            dirty_rects = self.draw()
            pg.display.update(dirty_rects)