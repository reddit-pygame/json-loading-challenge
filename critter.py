import itertools as it
from random import randint, choice
import pygame as pg
import tools, prepare


class Critter(pg.sprite.DirtySprite):
    """Parent class for Rabbits and Wolves."""
    velocities = {"left": (-1, 0),
                       "right": (1, 0),
                       "up": (0, -1),
                       "down": (0, 1)}
    def __init__(self, pos, direction, food, age, *groups):
        super(Critter, self).__init__(*groups)
        self.pos = pos
        self.direction = direction
        self.food = food
        self.max_food = 1000
        self.age = age
        self.dirty = 1
        self.image_cycle = it.cycle(self.images[self.direction])
        self.image = next(self.image_cycle)
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0
        self.eating = False
        self.fertility = 0
        
    def change_direction(self, direction=None):
        """
        If a direction is passed, switch to that direction. Otherwise,
        select a random direction.
        """        
        if direction:
            self.direction = direction
        else:    
            self.direction = choice(("left", "right", "up", "down"))
        self.image_cycle = it.cycle(self.images[self.direction])
        self.image = next(self.image_cycle)
        self.rect = self.image.get_rect(center=self.pos)
        self.dirty = 1
        
    def move(self):
        """
        Move sprite and keep it inside the screen area.
        """
        sr = prepare.SCREEN.get_rect()
        if self.rect.top < sr.top:
            self.change_direction("down")
        elif self.rect.bottom > sr.bottom:
            self.change_direction("up")
        elif self.rect.left < sr.left:
            self.change_direction("right")
        elif self.rect.right > sr.right:
            self.change_direction("left")    
        x, y = self.pos
        xvel, yvel = self.velocities[self.direction]
        x += self.speed * xvel
        y += self.speed * yvel
        self.pos = (x, y)
        self.rect.center = self.pos
        
    def move_to_other(self, other):
        if self.direction == "left":
            self.rect.left = other.rect.right
        elif self.direction  == "right":
            self.rect.right = other.rect.left
        elif self.direction == "up":
            self.rect.top = other.rect.bottom
        elif self.direction == "down":
            self.rect.bottom = other.rect.top
        self.pos = self.rect.center
        self.dirty = 1
        
    def base_update(self, dt, prey):
        """
        This update applies to all Critters and is
        called by Wolf.update and Rabbit.update.
        """
        self.age += 1
        if self.age > self.reproductive_age:
            self.fertility += 1       
        if not self.eating:
            if randint(0, 100) <= self.turn_chance:
                self.change_direction()
            self.timer += dt
            if self.timer >= self.animation_time:
                self.timer -= self.animation_time
                self.image = next(self.image_cycle)
                self.dirty = 1
            self.move()
            self.food -= self.hunger
            if self.food < self.max_food // 2:
                for food in prey:
                    if self.rect.colliderect(food.rect):
                        self.eating  = True
                        self.image = self.images["eating"][self.direction]
                        self.move_to_other(food)
                        self.food_source = food
                        break
        if self.food <= 0 or self.age >= self.expiration_age:
            self.kill()
            

class Wolf(Critter):
    images = {}
    images["eating"] = {}
    sizes = [(64, 32), (64, 32), (32, 64), (32, 64)]
    columns = (5,5,4,4)
    for direct, size, num_columns in zip(("right", "left", "up", "down"), sizes, columns):
        sheet = prepare.GFX["wolf{}".format(direct)]
        frames = tools.strip_from_sheet(sheet, (0, 0), size, num_columns)
        images[direct] = frames
        images["eating"][direct] = frames[0]

    def __init__(self, pos, direction, food, age, *groups):
        super(Wolf, self).__init__(pos, direction, food, age, *groups)
        self.turn_chance = 3
        self.animation_time = 50
        self.speed = 3
        self.hunger = 1
        self.reproduction_chance = 1
        self.reproductive_age = 2000
        self.gestation_period = 2000
        self.expiration_age = 15000   
        
    def update(self, dt, rabbits):
        self.base_update(dt, rabbits)
        if self.eating:
            prey = self.food_source
            self.food = min(self.max_food, self.food + prey.food) 
            prey.kill()
            self.eating = False
            self.change_direction()
            
            
class Rabbit(Critter):
    images = {}
    images["eating"] = {}
    sizes = [(32, 32), (32, 32), (19, 32), (19, 32)]
    for direct, size in zip(("right", "left", "up", "down"), sizes):
        sheet = prepare.GFX["rabbit{}".format(direct)]
        frames = tools.strip_from_sheet(sheet, (0, 0), size, 4)
        images[direct] = frames
        images["eating"][direct] = frames[0]
        
    def __init__(self, pos, direction, food, age, *groups):
        super(Rabbit, self).__init__(pos, direction, food, age, *groups)
        self.turn_chance = 3
        self.animation_time = 50
        self.speed = 2
        self.hunger = 1
        self.reproduction_chance = 6
        self.reproductive_age = 600
        self.gestation_period = 500
        self.expiration_age = 10000

    def update(self, dt, prey):
        self.base_update(dt, prey)
        if self.eating:
            source = self.food_source
            hunger = self.max_food - self.food
            eaten = min(hunger, source.growth)
            self.food += eaten
            self.food = min(self.food, self.max_food)
            source.growth = max(0, source.growth - eaten)
            self.eating = False
            self.change_direction()
        