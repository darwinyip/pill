import pygame, sys, os.path
from pygame.locals import *
from random import randint

SCREENRECT = Rect(0,0,600,600)

def load_image(file):
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image ""%s" %s'%(file, pygame.get_error())
    return surface.convert()

class Eater(pygame.sprite.Sprite):
	images = []
	speed = 5

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[0] # Surface
		self.rect = self.image.get_rect(center=SCREENRECT.center)

	def move(self, x_direction, y_direction):
		self.rect.move_ip(x_direction * self.speed, y_direction * self.speed)

	def get_position(self):
		return self.rect.center

class Pill(pygame.sprite.Sprite):
	image = []

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[0] # Surface
		
	def spawn(self):
		self.rect = self.image.get_rect(center=(SCREENRECT.w-randint(10,590),SCREENRECT.h-randint(10,590)))

class Score():
	score = 0

	def __init__(self):
		self.font = pygame.font.SysFont('Century Schoolbook', 32)

	def get_surface(self):
		return self.font.render(str(self.score), True, (0,0,0))
		 

	def update_score(self):
		self.score += 1

def main():
	pygame.init()
	pygame.display.set_caption('Pill')

	#Create window
	screen = pygame.display.set_mode(SCREENRECT.size)
	screen.fill((0,0,0))

	#Create background
	background = pygame.Surface(screen.get_size())
	background.fill((255,255,255))
	screen.blit(background,(0,0))

	#Create Score
	score = Score()
	screen.blit(score.get_surface(),(5,5))
	pygame.display.update()

	#Create groups
	all_sprites = pygame.sprite.RenderUpdates()

	#Create Eater
	Eater.images = [load_image('eater.png')]
	eater = Eater()

	#Create Pill
	Pill.images = [load_image(('pill.png'))]
	pill = Pill()
	pill.spawn()

	#Assign groups
	all_sprites.add(eater)
	all_sprites.add(pill)

	clock = pygame.time.Clock()

	#Game logic
	while(True):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		keystate = pygame.key.get_pressed()

		x_direction = keystate[K_RIGHT] - keystate[K_LEFT]
		y_direction = keystate[K_DOWN] - keystate[K_UP]

		eater.move(x_direction, y_direction)

		if pygame.sprite.collide_rect(eater,pill):
			score.update_score()
			background.fill((randint(0,190),randint(0,190),randint(0,190)))
			screen.blit(background,(0,0))
			screen.blit(score.get_surface(),(5,5))
			pygame.display.flip()
			pill.spawn()	

	 	all_sprites.clear(screen,background)
		dirty = all_sprites.draw(screen)
		pygame.display.update(dirty)
		clock.tick(60)

if __name__ == '__main__': main()