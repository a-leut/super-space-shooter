import pygame
import helpers

class World():
    image = None
    
    @classmethod
    def load_images(cls):
    	World.image = helpers.load_image('startile.png')
    
    def __init__(self, w, h):
        self.tile = World.image
        self.tileside = self.tile.get_height()
        self.ycounter = self.xcounter = 0
        self.map = pygame.Surface((w + 2*self.tileside, h + 2*self.tileside)).convert()
        for x in range(w/self.tileside + 2):
            for y in range(h/self.tileside + 2):
                self.map.blit(self.tile, (x*self.tileside, y*self.tileside))
                
    def move_camera(self, offset):
        self.xcounter = (self.xcounter - offset[0]*.75) % self.tileside
        self.ycounter = (self.ycounter - offset[1]*.75) % self.tileside

    def move_camera_y(self, n):
        self.ycounter = (self.ycounter - n) % self.tileside
        
    def move_camera_x(self, n):
        self.xcounter = (self.xcounter - n) % self.tileside
    
    def draw(self, screen):
        screen.blit(self.map, (self.xcounter - self.tileside, -self.ycounter))

