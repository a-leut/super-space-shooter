import math
import pygame
import random
from actor import Actor
from vector import Vector

class Shooter(Actor):
	img = []
	def __init__(self, screen):
		self._screen_w = screen.get_rect().width
		self._screen_h = screen.get_rect().height
		# start in dumb random place, needs changed later
		pos = (random.randint(0, self._screen_w) + self._screen_w*random.choice((-1, 1)),
			   random.randint(0, self._screen_h) + self._screen_h*random.choice((-1, 1)))	
		# Initialize an actor with these values
		Actor.__init__(self, Shooter.img[0], pos, 0)
		
