import pygame, random
from helpers import *

class P():
    def __init__(self, img):
        self._image = img
        self._lifetime = None
        self._decay = None
        self._rect = self._image.get_rect()
        self._vx, self._vy = None, None
        self.active = False
    def create(self, pos, life=100):
        self._lifetime = life
        self._decay = 10
        self._rect.topleft = pos
        self._ax = random.gauss(0, 1)
        self._ay = random.gauss(0, 1)
        self._vx = random.gauss(0, .3)
        self._vy = random.gauss(0, .3)
       # print self._vx, self._vy
        self.active = True
    def update(self):
        if self.active:
            self._vx += self._ax
            self._vy += self._ay
            self._rect.top += self._vy
            self._rect.left += self._vx
            self._lifetime -= self._decay
            if self._lifetime < 0:
                self.active = False
    def draw(self, screen):
        if self.active:
            screen.blit(self._image, self._rect)

class KamaExploder():
    img1 = None
    img2 = None
    img3 = None
    @classmethod
    def load_images(cls):
        KamaExploder.img1 = load_image("particle0000.png")
        KamaExploder.img2 = load_image("particle0001.png")
        KamaExploder.img3 = load_image("particle0002.png")
    def __init__(self, n):
        self._parts = []
        self._num_parts = n
        for n in xrange(0, 10000):
            if n % 3 == 0:
                img = KamaExploder.img1
            elif n % 3 == 1:
                img = KamaExploder.img2
            else:
                img = KamaExploder.img3
            self._parts.append(P(img))
    def create(self, pos):
        n = 0
        # look for unused particles
        while self._parts[n].active == True and n + self._num_parts < 10000:
            n += self._num_parts
        for i in xrange(n, n + self._num_parts):
            self._parts[i].create(pos)
    def update(self):
        for p in self._parts:
            p.update()
    def draw(self, screen):
        for p in self._parts:
            p.draw(screen)
            
class PlayerExploder():
    img1 = None
    img2 = None
    @classmethod
    def load_images(cls):
        PlayerExploder.img1 = load_image("particle0001.png")
        PlayerExploder.img2 = load_image("particle0002.png")
    def __init__(self):
        self._parts = []
        for n in xrange(0, 200):
            if n % 2 == 0:
                img = PlayerExploder.img1
            else:
                img = PlayerExploder.img2
            self._parts.append(P(img))
    def create(self, pos):
        for p in self._parts:
            p.create(pos, 10000)
    def update(self):
        for p in self._parts:
            p.update()
    def draw(self, screen):
        for p in self._parts:
            p.draw(screen)
            