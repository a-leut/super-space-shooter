import os.path, pygame, math, sys, random
from actor import Actor
from kama import Kama
from world import World
from playership import PlayerShip, Bullet, Arrow, HealthBar
from powerups import Time
from particles import P, KamaExploder, PlayerExploder
from helpers import *

if __name__ == '__main__':
	# Constants
	WIDTH = 800
	HEIGHT = 600
	FPS = 30
	KAMA_SPAWN_RATE = 10
	GAME_STATE = -1
	SCORE = 0 #should probably be something other than a global

	# Initialize general game modules
	pygame.init()
	pygame.mixer.init()

	#screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 32)
	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	clock = pygame.time.Clock()
	inputhandler = InputHandler()
	move_timer = MoveTimer()

	# Load images
	PlayerShip.load_images()
	World.load_images()
	Kama.load_images()
	MiniMap.load_images()
	Bullet.load_images()
	Arrow.load_images()
	Time.load_images()
	HealthBar.load_images()
	KamaExploder.load_images()
	PlayerExploder.load_images()

	# Load sounds
	PlayerShip.laser_sound = load_sound('lasersound.wav')
	explode_sound = load_sound('enemyexplode.wav')
	time_sound = load_sound('powerup.wav')
	collide_sound = load_sound('hitship.wav')
	explode_sound.set_volume(0.25)
	PlayerShip.laser_sound.set_volume(0.1)
	time_sound.set_volume(0.45)
	
	# Load font
	font_path = os.path.join('data', "pixelfont.ttf")
	font = pygame.font.Font(font_path, 32)
	
	# countdown timer
	class Countdown:
		def __init__(self):
			self._time_left = 30
			self._total_time = 0
			self._time_added = 11
		def dec(self):
			self._time_left -= 1
			self._total_time += 1
		def inc(self):
			self._time_left += self._time_added 
			if self._time_left > 30:
				self._time_left = 30
				self._time_added -= 1
		def get(self):
			return self._time_left

	# Create objects
	player = PlayerShip((WIDTH/2, HEIGHT/2), 0, FPS)
	arrow = Arrow((WIDTH/2, HEIGHT/2))
	world = World(WIDTH, HEIGHT)
	minimap = MiniMap(WIDTH, HEIGHT)
	healthbar = HealthBar((7, 48))
	exploder = KamaExploder(100)
	player_exploder = PlayerExploder()

	# Object groups
	bullets = pygame.sprite.Group()
	Bullet.group = bullets
	kamas = pygame.sprite.Group()
	kamas_on_minimap = pygame.sprite.Group()
	visible_kamas = pygame.sprite.Group()
	Kama.group = kamas
	Kama.on_minimap = kamas_on_minimap 
	Kama.visible = visible_kamas

	kama_counter = KAMA_SPAWN_RATE
	max_kamas_on_map = 13
	
	# time_power stuff
	time_power = None
	coin_placed = False
		
	countdown = Countdown()
	pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	pygame.time.set_timer(pygame.USEREVENT+2, 60000)
	
	# Set up event handlers
	inputhandler.input_subscribers = [player.give_input]
	inputhandler.mouse_move_subscribers = [player.update]

	# Draw background
	#screen.blit(world.map, (0, world.tileside - world.ycounter))
	#pygame.display.update()
	
	splash = load_image("splashscreen.png")
	screen.blit(splash, splash.get_rect())
	pygame.display.update()
	
	while GAME_STATE == -1:
		elapsed_time = clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					GAME_STATE = 1
	
	while 1:	
		while GAME_STATE == 1:
			elapsed_time = clock.tick(FPS)
	
			# Get input
			inputhandler.Update(pygame.event.get(), countdown)
			
			# Spawn stuff
			kama_counter -= 1
			if kama_counter <= 0 and len(kamas_on_minimap) < max_kamas_on_map:
				Kama(screen, player.get_vector()).add_to_group()
				kama_counter = KAMA_SPAWN_RATE
	
			# Update stuff
			player.update(None)
			move_timer.update(player._vector)
			exploder.update()
			bullets.update(screen)
	
			# keep placing time
			if coin_placed == False:
				pos = (random.randint(-3*screen.get_rect().width, 3*screen.get_rect().width),
					   random.randint(-2*screen.get_rect().height, 3*screen.get_rect().height))
				time_power = Time(pos)
				coin_placed = True
			
			# point arrow to coin
			angle_towards_time_power = math.atan2(time_power.rect.left-(WIDTH/2),
												  time_power.rect.top-(HEIGHT/2)) - math.pi
			arrow.rotate_to(angle_towards_time_power)
				
			# Update stuff around the player
			player_offset = player.get_offset()
			world.move_camera(player_offset)
			kamas.update(player_offset)
			time_power.update(player_offset)
			
			# Collide visible kamas with player and bullets
			for k in visible_kamas:
				if pygame.sprite.collide_circle(k, player):
					exploder.create(k.rect.topleft)
					k.remove(kamas)
					k.remove(visible_kamas)
					k.remove(kamas_on_minimap)
					collide_sound.play()
					player.health -= 1
					healthbar.set_health(player.health)
				for b in bullets:
					if pygame.sprite.collide_circle(k, b):
						b.remove(bullets)
						exploder.create(k.rect.topleft)
						k.do_damage(1)
						explode_sound.play()
						SCORE += 10
			
			# Check player and coin
			if pygame.sprite.collide_circle(time_power, player):
				time_sound.play()
				countdown.inc()
				coin_placed = False
	
			if player.health <= 0 or countdown.get() < 0:
				explode_sound.play()
				GAME_STATE = 0
	
			#Draw objects
			world.draw(screen)
			visible_kamas.draw(screen)
			player.draw(screen)
			exploder.draw(screen)
			bullets.draw(screen)
			time_power.draw(screen)
	
			# Draw ui stuff
			distance = math.sqrt((WIDTH/2 - time_power.rect.centerx)**2 + (HEIGHT/2 - time_power.rect.centery)**2)
			if distance > 400:
				arrow.draw(screen)
			if time_power.rect.left > -2*WIDTH and time_power.rect.right < 3*WIDTH \
			and time_power.rect.top > -2*HEIGHT and time_power.rect.bottom < 3*HEIGHT:
				minimap.draw(screen, kamas_on_minimap, time_power)
			else:
				minimap.draw(screen, kamas_on_minimap)
			healthbar.draw(screen)
	
			# Render the text
			#text = font.render("Health: %d Score %d" % (player.health, SCORE), True, (255,255,255))
			text = font.render("Time: %d Score: %d" % (countdown.get(), SCORE), True, (255,255,255))
			textRect = text.get_rect()
			textRect.topleft = (5, 5)
			screen.blit(text, textRect)
	
			pygame.display.update()
		
		player_exploder.create((WIDTH/2, HEIGHT/2))
		
		while GAME_STATE == 0:
			elapsed_time = clock.tick(FPS)
			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						# Create objects
						player = PlayerShip((WIDTH/2, HEIGHT/2), 0, FPS)
						arrow = Arrow((WIDTH/2, HEIGHT/2))
						world = World(WIDTH, HEIGHT)
						minimap = MiniMap(WIDTH, HEIGHT)
						healthbar = HealthBar((7, 48))
						exploder = KamaExploder(100)
						player_exploder = PlayerExploder()
					
						# Object groups
						bullets = pygame.sprite.Group()
						Bullet.group = bullets
						kamas = pygame.sprite.Group()
						kamas_on_minimap = pygame.sprite.Group()
						visible_kamas = pygame.sprite.Group()
						Kama.group = kamas
						Kama.on_minimap = kamas_on_minimap 
						Kama.visible = visible_kamas
					
						kama_counter = KAMA_SPAWN_RATE
						max_kamas_on_map = 13
						
						# time_power stuff
						time_power = None
						coin_placed = False
							
						countdown = Countdown()
						pygame.time.set_timer(pygame.USEREVENT+1, 1000)
						pygame.time.set_timer(pygame.USEREVENT+2, 60000)
						
						# Set up event handlers
						inputhandler.input_subscribers = [player.give_input]
						inputhandler.mouse_move_subscribers = [player.update]
					
						# Draw background
						screen.blit(world.map, (0, world.tileside - world.ycounter))
						GAME_STATE = 1
				if event.type == pygame.QUIT: 
					sys.exit()
			
			player_exploder.update()
			
			world.draw(screen)
			visible_kamas.draw(screen)
			player_exploder.draw(screen)
			
			score = font.render("Score: %d" % SCORE, True, (255,255,255))
			scoreRect = text.get_rect(center=(WIDTH/2, HEIGHT/2-40))
			screen.blit(score, scoreRect)
			lasted = font.render("Lasted %d seconds" % countdown._total_time, True, (255,255,255))
			lastedRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
			screen.blit(lasted, lastedRect)
			press = font.render("Press space to play again", True, (255,255,255))
			pressRect = text.get_rect(center=(WIDTH/2, HEIGHT/2+40))
			screen.blit(press, pressRect)

			
			pygame.display.update()

		

print 'You lose, sucker'
sys.exit()