from random import randint, choice
import json
import pygame as pg

import tools, prepare
from state_engine import GameState
from labels import Button, ButtonGroup
from grass import Grass
from critter import Rabbit, Wolf


def random_pos(rect):
    return randint(rect.left, rect.right), randint(rect.top, rect.bottom)


class MenuScreen(GameState):
    """
    First state of the game. It allows the user to start a new simulation
    or load a previously saved simulation.
    """    
    def __init__(self):
        super(MenuScreen, self).__init__()
        self.next_state = "SIM"
        self.screen_rect = prepare.SCREEN.get_rect()
        style = {"text_color": pg.Color("gray80"),
                    "fill_color": pg.Color("gray10"),
                    "hover_fill_color": pg.Color("gray20"),
                    "hover_text_color": pg.Color("gray90")}
        self.buttons = ButtonGroup()
        w, h = 200, 80
        space = 50
        left = self.screen_rect.centerx - (w//2)
        top = self.screen_rect.centery - (h + space)
        Button((left, top, w, h), self.buttons, text="New Sim",
                  hover_text="New Sim", call=self.new_game, **style)
        top += h + space + space
        Button((left, top, w, h), self.buttons, text="Load Sim", 
                  hover_text="Load Sim", call=self.load_game, **style)
            
    def new_game(self, *args):
        """
        Set up the populations for a new sim to be passed to the Sim state.
        """
        rect = self.screen_rect.inflate(-64, -64)
        num_grass = 50
        num_rabbits = 20
        num_wolves = 1
        grasses = pg.sprite.Group()
        rabbits = pg.sprite.Group()
        wolves = pg.sprite.Group()
        for g in range(num_grass):
            Grass(random_pos(rect), 1000, grasses)
        for r in range(num_rabbits):
            direction = choice(("left", "right", "up", "down"))
            Rabbit(random_pos(rect), direction, 1000, 0, rabbits)
        for f in range(num_wolves):
            direction = choice(("left", "right", "up", "down"))
            Wolf(random_pos(rect), direction, 1000, 0, wolves)
        self.persist["grasses"] = grasses
        self.persist["rabbits"] = rabbits
        self.persist["wolves"] = wolves
        self.done  = True
            

    def load_game(self, *args):
        """
        Load the previously saved populations from JSON and 
        pass them to the Sim state by adding them to self.persist. 
        """
        pass
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        #Treat the whole screen as dirty
        dirty = [surface.get_rect()]
        self.buttons.draw(surface)
        return dirty