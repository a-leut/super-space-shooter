import math
import pygame
from actor import Actor
from helpers import *

class Time(Actor):
    img = None
    @classmethod
    def load_images(cls):
        Time.img = load_image("time.png", -1)
    
    def __init__(self, pos):
        Actor.__init__(self, Time.img, pos, 0)

    def update(self, offset):
        self.rect.topleft = (self.rect.left - offset[0], self.rect.top + offset[1])
