import math
import pygame
import random
from actor import Actor
from helpers import *

class Kama(Actor):
	img_normal = []
	img_charge = []
	
	#groups
	group = None
	on_minimap = None
	visible = None
	
	@classmethod
	def load_images(cls):
		kama_normal = load_image('enemy0000.png', -1)
		kama_charge = load_image('enemy0001.png', -1)
		# Catch 360 rotated versions of the images
		for n in range(359):
			Kama.img_normal.append(pygame.transform.rotate(kama_normal, n))
			Kama.img_charge.append(pygame.transform.rotate(kama_charge, n))
	
	def __init__(self, screen, player_vector=None):
		self._screen_w = screen.get_rect().width
		self._screen_h = screen.get_rect().height


		# 1337 = uninitialized... i hope no one ever sees this
		if player_vector and player_vector.mag > 1:
			# Spawn on the side of the screen that player is traveling
			# Using a really shitty heuristic that splits where the player can
			# move into 4 quads.
			if abs(player_vector.angle) < math.pi/4:
				#right
				pos = (3*screen.get_rect().width, random.randint(-2*screen.get_rect().height, 3*screen.get_rect().height))
			elif player_vector.angle >= math.pi/4 and player_vector.angle <	3*math.pi/4:
				# up
				pos = (random.randint(-2*screen.get_rect().width, 3*screen.get_rect().width), -2*screen.get_rect().height)
			elif abs(player_vector.angle) >= 3*math.pi/4 and abs(player_vector.angle) < 5*math.pi/4:
				# left
				pos = (-2*screen.get_rect().width, random.randint(-2*screen.get_rect().height, 3*screen.get_rect().height))
			else:
				# down
				pos = (random.randint(-2*screen.get_rect().width, 3*screen.get_rect().width), 3*screen.get_rect().height)
		else:
			pos = (random.randint(0, screen.get_rect().width) + screen.get_rect().width*random.choice((-2, 2)),
				   random.randint(0, screen.get_rect().height) + screen.get_rect().height*random.choice((-1, 2)))
		
		# point towards center
		initial_orient = math.atan2((self._screen_h/2)-pos[1], (self._screen_w/2)-pos[0])

		# Initialize an actor with these values
		Actor.__init__(self, Kama.img_normal[0], pos, initial_orient)
		
		self._roam_speed = 5
		self._follow_speed = 3.5
		self._charge_speed = 10
		self._health = 0
		self._ROAM, self._FOLLOW, self._CHARGE = 0, 1, 2
		self._refollowed = False

		self._vector = Vector(self._roam_speed, self._angle)
		self._mode = self._ROAM
		
		center = self.rect.center
		self.image = Kama.img_normal[int(math.degrees(-self._angle - math.pi/2))]
		self.rect = self.image.get_rect(center = center)
		self.radius = self.img_normal[0].get_rect().height/2

	def do_damage(self, damage):
		self._health -= damage

	def update(self, offset):
		distance = math.sqrt((self._screen_w/2 - self.rect.centerx)**2 + (self._screen_h/2 - self.rect.centery)**2)
		
		if self._mode == self._ROAM and distance < 600:
			self._mode = self._FOLLOW
			
		if self._mode == self._FOLLOW:
			if distance < 200:
				self._angle = math.atan2((self._screen_h/2)-self.rect.top, (self._screen_w/2)-self.rect.left)
				self._vector = Vector(self._charge_speed, self._angle)
				self.image = Kama.img_charge[int(math.degrees(-self._angle - math.pi/2))]
				self._mode = self._CHARGE
			else:
				self._angle = math.atan2((self._screen_h/2)-self.rect.top, (self._screen_w/2)-self.rect.left)
				self._vector = Vector(self._follow_speed, self._angle)
				self.image = Kama.img_normal[int(math.degrees(-self._angle - math.pi/2))]
			
		if self._mode == self._CHARGE and distance > 500:
			if self._refollowed:
				self.mode = self._ROAM
				self._angle = random.random() % math.pi*2
				self._vector = Vector(self._roam_speed, self._angle)
			else:
				self._vector = Vector(self._follow_speed, random.random() % 2*math.pi)
				self.image = Kama.img_normal[int(math.degrees(-self._angle - math.pi/2))]
				self._mode = self._FOLLOW
				self._refollowed = True
	
		self.rect.topleft = (self.rect.left + self._vector.x - offset[0], self.rect.top + self._vector.y + offset[1])

		# Check if within 4x4 grid of screens
		if self.rect.left < -3*self._screen_w or self.rect.right > 4*self._screen_w \
		or self.rect.top < -3*self._screen_h or self.rect.bottom > 4*self._screen_h:
			self.remove(Kama.group)
		
		# Check if within 3x3 grid of screens
		if self not in Kama.on_minimap:
			if self.rect.left > -2*self._screen_w and self.rect.right < 3*self._screen_w \
			and self.rect.top > -2*self._screen_h and self.rect.bottom < 3*self._screen_h:
				self.add(Kama.on_minimap)
		elif self in Kama.on_minimap:
			if self.rect.left < -2*self._screen_w or self.rect.right > 3*self._screen_w \
			or self.rect.top < -2*self._screen_h or self.rect.bottom > 3*self._screen_h:
				self.remove(Kama.on_minimap)
		
		if self._health < 0:
			self.remove(Kama.group)
			if self in Kama.on_minimap:
				self.remove(Kama.on_minimap)
				if self in Kama.visible:
					self.remove(Kama.visible)

		
		if self in Kama.group:
			# Check if on screen, if so add to visible sprite group and vice versa
			if self not in Kama.visible:
				if self.rect.right > 0 and self.rect.left < self._screen_w \
				and self.rect.bottom > 0 and self.rect.top < self._screen_h:
				#if self.rect.left > 0 and self.rect.right < self._screen_w:
					self.add(Kama.visible)
			elif self in Kama.visible:
				if self.rect.right < 0 or self.rect.left > self._screen_w \
				or self.rect.bottom < 0 or self.rect.top > self._screen_h:
				#if self.rect.left < 0 or self.rect.right > self._screen_w:
					self.remove(Kama.visible)

	def add_to_group(self):
		if Kama.group is not None:
			self.add(Kama.group)

	