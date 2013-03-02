import os.path, pygame, math, world, sys

MAKE_MODE = True

class Vector():
	def __init__(self, mag, angle):
		self.mag = mag
		self.angle = angle
		self.x = math.cos(angle)*mag
		self.y = math.sin(angle)*mag
	
	def product(v1, v2):
		p_x = v1.x + v2.x
		p_y = v1.y + v2.y
		return Vector(math.sqrt(p_x**2 + p_y**2), math.atan2(p_y, p_x))
		
class MoveTimer():
	def __init__(self):
		self.xsubscribers, self.ysubscribers = [], []
	
	def update(self, vector):
		for subscriber in self.xsubscribers:
			#subscriber(math.cos(vector.angle)*vector.mag)
			subscriber(vector.x)
		
		for subscriber in self.ysubscribers:
			#subscriber(math.sin(vector.angle)*vector.mag)
			subscriber(vector.y)
			
class MiniMap:
	img_bg = None
	img_enemy = None
	img_player = None
	
	@classmethod
	def load_images(cls):
		MiniMap.img_bg = load_image('minimap.png')
		MiniMap.img_enemy = load_image('enemyicon.png')
		MiniMap.img_player = load_image('playericon.png')
		MiniMap.img_time = load_image('timeicon.png')
		MiniMap.img_bg.set_alpha(128)
	
	def __init__(self, w, h):
		self._padding = 10
		self.bg_image = MiniMap.img_bg
		self.enemy_image = MiniMap.img_enemy
		self.player_image = MiniMap.img_player
		self.time_image = MiniMap.img_time
		self.bg_image_rect = self.bg_image.get_rect(topleft=(w - self.bg_image.get_width() - self._padding,
												 h - self.bg_image.get_height() - self._padding))
		self.enemy_image_rect = self.enemy_image.get_rect(topleft=self.bg_image_rect.topleft)
		self.time_image_rect = self.time_image.get_rect(topleft=self.bg_image_rect.topleft)
		self.player_image_rect = self.player_image.get_rect(center=self.bg_image_rect.center)
		self._x_tile = float(self.bg_image_rect.width)/5
		self._y_tile = float(self.bg_image_rect.height)/5
		self._x_scale = self._x_tile/w
		self._y_scale = self._y_tile/h
		
	def draw(self, screen, enemies, time=None):
		screen.blit(self.bg_image, self.bg_image_rect.topleft)
		for e in enemies:
			offset = (e.rect.left*self._x_scale + 2*self._x_tile, e.rect.top*self._y_scale + 2*self._y_tile)
			screen.blit(self.enemy_image, self.enemy_image_rect.move(offset))
		if time:
			offset = (time.rect.left*self._x_scale + 2*self._x_tile, time.rect.top*self._y_scale + 2*self._y_tile)
			screen.blit(self.time_image, self.enemy_image_rect.move(offset))
		screen.blit(self.player_image, self.player_image_rect)

class InputHandler:
	def __init__ (self):
		self._current_direction_key = None
		self._key_stack = []
		self._is_mouse_down = False
		self.mouse_move_subscribers = []
		self.input_subscribers = []
	def Update (self, events, countdown):
		for event in events:
			if event.type == pygame.QUIT: 
				sys.exit()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self._is_mouse_down = True
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self._is_mouse_down = False
			
			if event.type == pygame.MOUSEMOTION:
				for subscriber in self.mouse_move_subscribers:
					subscriber(pygame.mouse.get_pos())
			
			if event.type == pygame.KEYDOWN:
				self._key_stack.append(event.key)
				self._current_direction_key = event.key
			if event.type == pygame.KEYUP:
				try:
					self._key_stack.remove(event.key)
				except:
					pass
			if self._key_stack == []:
				self._current_direction_key = None
			elif self._current_direction_key != self._key_stack[-1]:
				self._current_direction_key = self._key_stack[-1]
			
			if event.type == pygame.USEREVENT+1:
				countdown.dec()
			if event.type == pygame.USEREVENT+2:
				countdown.dec_time_added()
	
		for subscriber in self.input_subscribers:
			subscriber(self._current_direction_key, self._is_mouse_down)

def load_image(file_name, colorkey=None):

	full_name = os.path.join('data', file_name)

	image = pygame.image.load(full_name)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image

def load_sound(file_name):
	full_name = os.path.join('data', file_name)
	return pygame.mixer.Sound(full_name)

def clear_rect(screen, rect):
	black = 0, 0, 0
	screen.fill(black, rect)
	
