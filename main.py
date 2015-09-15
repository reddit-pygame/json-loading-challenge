import sys
import pygame as pg

from state_engine import Game, GameState
import prepare
import menu, sim

states = {"MENU": menu.MenuScreen(),
              "SIM": sim.Sim()}
              
game = Game(prepare.SCREEN, states, "MENU")
game.run()
pg.quit()
sys.exit()