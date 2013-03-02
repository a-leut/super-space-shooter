import math
import pygame
from actor import Actor
from helpers import *

class Arrow(Actor):
    img = None
    
    @classmethod
    def load_images(cls):
        arrow = load_image('arrow.png', -1)
        padded_image = pygame.Surface((arrow.get_width(), arrow.get_height() + 300))
        padded_image.blit(arrow, arrow.get_rect().topleft)
        padded_image.convert()
        padded_image.set_colorkey(padded_image.get_at((0,0)), pygame.RLEACCEL)
        #padded_image.set_alpha(128)
        Arrow.img = padded_image
    
    def __init__(self, initial_pos):
        Actor.__init__(self, Arrow.img, initial_pos, 0)
        
    def rotate_to(self, angle):
        self._angle = angle
        center = self.rect.center
        self.image = pygame.transform.rotate(self._loaded_image, math.degrees(self._angle))
        self.rect = self.image.get_rect(center=center)
        
class HealthBar(Actor):
    imgs = []
    
    @classmethod
    def load_images(cls):
        HealthBar.imgs.append(load_image("heart0000.png", -1))
        HealthBar.imgs.append(load_image("heart0001.png", -1))
        HealthBar.imgs.append(load_image("heart0002.png", -1))
        HealthBar.imgs.append(load_image("heart0003.png", -1))
        HealthBar.imgs.append(load_image("heart0004.png", -1))

    def __init__(self, pos):
        Actor.__init__(self, HealthBar.imgs[4], (0,0), 0)
        self.rect.topleft = pos
    
    def set_health(self, n):
        self.image = HealthBar.imgs[n-1]


class Bullet(Actor):
    group = None
    img = []
    
    @classmethod
    def load_images(cls):
        bullet_image = load_image('laser.png', -1)
        # Catch 720 rotated versions of the bullet image
        for n in range(0, 719):
            m = n/2
            Bullet.img.append(pygame.transform.rotate(bullet_image, m))
    
    def __init__(self, initial_position, vector_shot_from):
        self._speed = 20
        Actor.__init__(self, Bullet.img[0], initial_position, vector_shot_from.angle)
        self._vector = Vector.product(Vector(self._speed, self._angle), vector_shot_from)
        center = self.rect.center
        self.image = Bullet.img[int(2*math.degrees(- self._angle - math.pi/2))]
        self.rect = self.image.get_rect(center=center)
        self.radius = (Bullet.img[0].get_rect().width + Bullet.img[0].get_rect().height)/4

    def update(self, screen):
        self.rect.topleft = (self.rect.left + self._vector.x, self.rect.top + self._vector.y)
        if self.rect.top < 0 or self.rect.bottom > screen.get_rect().height \
        or self.rect.left < 0 or self.rect.right > screen.get_rect().width:
            self.remove(Bullet.group)
    
    def add_to_group(self):
        if Bullet.group is not None:
            self.add(Bullet.group)

class PlayerShip(Actor):
    img_normal = None
    img_thrust = None
    img_lstrafe = None
    img_rstrafe = None
    
    @classmethod
    def load_images(cls):
        PlayerShip.img_normal = load_image('ship0000.png', -1)
        PlayerShip.img_thrust = load_image('ship0001.png', -1)
        PlayerShip.img_lstrafe = load_image('ship0003.png', -1)
        PlayerShip.img_rstrafe = load_image('ship0002.png', -1)

    def __init__(self, initial_position, initial_orientation, fps):
        Actor.__init__(self, PlayerShip.img_normal, initial_position, initial_orientation)
        self._loaded_t = PlayerShip.img_thrust
        self._loaded_ls = PlayerShip.img_lstrafe
        self._loaded_rs = PlayerShip.img_rstrafe
        self._cur_image = self._loaded_image
        
        self._vector = Vector(0, 0)
        self._max_speed = 13
        self._acceleration_rate = 0.5
        self._fire_rate = 50
        self._time_since_fire = 0
        
        self.health = 5
        self.radius = (self._loaded_image.get_rect().width + self._loaded_image.get_rect().height)/4
        
    def update(self, mouse_pos = None):
        elapsed_time = pygame.time.get_ticks()
        if mouse_pos is not None:
            self._angle = math.pi - math.atan2(self.rect.centery-mouse_pos[1], self.rect.centerx-mouse_pos[0])
        center = self.rect.center
        self.image = pygame.transform.rotate(self._cur_image, math.degrees(self._angle - math.pi/2))
        self.rect = self.image.get_rect(center=center)
    
    def accelerate(self, rel_angle = None):
        if rel_angle is None:
            cur_vector = Vector(self._acceleration_rate, self._angle)
        else:
            cur_vector = Vector(self._acceleration_rate, self._angle + rel_angle)
        new_vector = Vector.product(self._vector, cur_vector)
        if new_vector.mag > self._max_speed:
            self._vector = Vector(self._max_speed, new_vector.angle)
        else:
            self._vector = new_vector
    
    def shoot(self):
        elapsed_time = pygame.time.get_ticks()
        if elapsed_time - self._time_since_fire > self._fire_rate:
            PlayerShip.laser_sound.play()
            Bullet(self.rect.center, Vector(0, -self._angle)).add_to_group()
            self._time_since_fire = elapsed_time
        
    def get_offset(self):
        return (self._vector.x, self._vector.y)
    
    def get_vector(self):
        return self._vector
    
    def give_input(self, dir_key, is_mouse_down):
        if dir_key == None:
            self._cur_image = self._loaded_image
        if dir_key == pygame.K_w:
            self._cur_image = self._loaded_t
            self.accelerate()
        if dir_key == pygame.K_a:
            self._cur_image = self._loaded_ls #left strafe image
            self.accelerate(math.pi/2)
        if dir_key == pygame.K_d:
            self._cur_image = self._loaded_rs #right strage image
            self.accelerate(-math.pi/2)
        if is_mouse_down == True:
            self.shoot()

        
        