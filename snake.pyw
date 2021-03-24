"""
copy of the famous snake game written in python

SOURCES / CREDITS:	
	Fonts:	-CamingoCode-Regular.ttf (Creative Commons Attribution - No Derivative Works 3.0 Unported,
				https://creativecommons.org/licenses/by-nd/3.0/) by Jan Fromme published on 
				https://www.fontsquirrel.com/fonts/camingocode (last visited: 20. Nov. 2020, 21:17 UTC+1)
				

	SFX: completely self produced with  Bosca Ceoil. (Creative Commons Attribution - No Derivative Works
			3.0 Unported, https://creativecommons.org/licenses/by-nd/3.0/)

TODO implement set_screen_scale
"""

# imports
import time
import scores
import random
import set_screen_scale
from pathlib import Path
# all this pygame stuff
import pygame
import pygame.freetype
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()


# window settings
WINDOW_TITLE = 'Snake - Python'		# set the window title
MULTIPLIER = 1.5	# this multiplier can be used to scale the game up / down
					# up or down. Any variable influencing the scale
					# will be multiplied with this

FPS = 60		# the frames per second

initial_blocks_per_second = 7		# the starting velocity
blocks_per_second = initial_blocks_per_second	# the velocity of the snake
						# will be increased by the acceleration value
acceleration = 1		# the acceleration value
update_time = 1 / blocks_per_second		# the time that passes between every snake update
last_time = 0			# store the last time the snake was moved
				
# game settings
set_wall_boundaries = False		# True: Snake dies at collision with wall
								# False: Snake will appear on the other side
set_increase_velocity = False	# True: Snake will accelerate after every bite
								# False: Snake won't accelerate
gen_path = str(Path(__file__).parent.absolute())
# game constants
# directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# defining colors
COL_BACKGROUND = (0,0,0)		# color of the background
COL_SNAKE = (0,255,0)			# color of the snake
COL_FOOD = (255,0,0)			# color of the food
COL_MENU_NORMAL = (255,255,255)		# color of the not highlighted text in menu
COL_MENU_HIGHLIGHTED = COL_SNAKE	# color of the selected / highlighted text in menu

# sound
SFX_EAT = pygame.mixer.Sound(gen_path + '/lib/sfx/eat.wav')																																					# eat it - just eat it
SFX_DIE = pygame.mixer.Sound(gen_path + '/lib/sfx/die.wav')

# coordinate system / blocks
BLOCKS_X = 35		# amount of blocks in width
BLOCKS_Y = 20		# 		-''-	in height
BLOCK_WIDTH = 20 * MULTIPLIER		# size of one block
BLOCK_MARGIN = BLOCK_WIDTH / 20		# room between the blocks divided by 2

# game variables
points = 0
menu_active = True		# used to switch between game and screen

# menu variables
menu_points = ["PLAY", "wall boundaries: False", "increase speed: False", "QUIT"]	# stores the different menu points
menu_i = 0		# stores wich point is chosen
menu_action = False		# stores whether the enter key in menu was pressed and the corresponding action needs to be done
menu_font = pygame.freetype.Font(gen_path + "/lib/fonts/CamingoCode-Regular.ttf", 30)

# window
SCREEN_WIDTH = int(BLOCK_WIDTH * BLOCKS_X)
SCREEN_HEIGHT = int(BLOCK_WIDTH * BLOCKS_Y)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# snake class
class Snake():
	""" snake-class
	controlling, drawing, growing the snake: all of this happens here
	"""

	def __init__(self, color):
		# syncing everything up and creating necessary variables
		self.color = color
		
		self.pos_x = []	# add the first block (this one and all following will be in COL_SNAKE)
		self.pos_y = []
		
		self.reset()

		self.direction = RIGHT		# the direction of the snake

		self.plan_add_block = False		# this variable is used to plan the next addition of a block
	
	def reset(self):
		self.pos_x.clear()			# delete the entire snake
		self.pos_y.clear()
		self.pos_x = [int(BLOCKS_X / 2)]		# add the first block (this one and all following will be in COL_SNAKE)
		self.pos_y = [int(BLOCKS_Y / 2)]
		self.pos_x.append(int(BLOCKS_X / 2) - 1)	# add the last block used to clean up behind the snake (this one will be in COL_BACKGROUND)
		self.pos_y.append(int(BLOCKS_Y / 2))
		self.direction = RIGHT		# reset direction

	def addBlock(self):
		""" add a block the snake """
		# take the position for the new block -> it's at the last erasing block
		add_pos_x = self.pos_x.pop(-1)
		add_pos_y = self.pos_y.pop(-1)
		# now insert the new block and the trailing block, since i'd just been popped out
		self.pos_x.append(add_pos_x)
		self.pos_y.append(add_pos_y)
		self.pos_x.append(-3)
		self.pos_y.append(-3)


	def move(self):
		""" moves the complete list """

		# set the difference of position for the first block
		dx = 0
		dy = 0
		if(self.direction == UP):
			dx = 0
			dy = -1
		elif(self.direction == DOWN):
			dx = 0
			dy = 1
		elif(self.direction == LEFT):
			dx = -1
			dy = 0
		elif(self.direction == RIGHT):
			dx = 1
			dy = 0
		
		# move all blocks to the position of the block before except the first one (backwards!)
		for i in range(len(self.pos_x)-1, 0, -1):
			self.pos_x[i] = self.pos_x[i-1]
			self.pos_y[i] = self.pos_y[i-1]
		
		# move the first block
		self.pos_x[0] += dx
		self.pos_y[0] += dy

		# wall collision / teleport
		if(set_wall_boundaries == True):
			pass	# the situation will be manged with in the collision part of main loop
					# if the snake should die when touching the wall
		else:
			# but the teleporting will be done here
			# first the x axis
			if(self.pos_x[0] < 0):
				self.pos_x[0] = BLOCKS_X - 1
			elif(self.pos_x[0] >= BLOCKS_X):
				self.pos_x[0] = 0
			# now the y-axis
			if(self.pos_y[0] < 0):
				self.pos_y[0] = BLOCKS_Y - 1
			elif(self.pos_y[0] >= BLOCKS_Y):
				self.pos_y[0] = 0

	def draw(self):
		""" drawing the snake block by block """
		for i in range(len(self.pos_x)):
			x = int((self.pos_x[i] * BLOCK_WIDTH) + BLOCK_MARGIN)
			y = int((self.pos_y[i] * BLOCK_WIDTH) + BLOCK_MARGIN)
			w = int(BLOCK_WIDTH - (2 * BLOCK_MARGIN))
			col = 0
			if(i == len(self.pos_x)-1):
				col = COL_BACKGROUND
			else:
				col = COL_SNAKE
			pygame.draw.rect(screen, col, (x,y,w,w))


# food class
class Food():
	""" food-class
	handles the placement and collision of the nice
	red bit for the snake to eat
	"""
	
	def __init__(self, color):
    	# syncing everything up and creating necessary variables
		self.color = color

		self.pos_x = 0
		self.pos_y = 0
  
	def generate(self):
		""" find a new position for the food and erase the old one"""
		position_okay = False
		while position_okay == False:
			self.erase(self.pos_x, self.pos_y)
			self.pos_x = random.randint(0, BLOCKS_X - 1)
			self.pos_y = random.randint(0, BLOCKS_Y - 1)

			# repeat if the snack is on the snake
			position_okay = True
			for i in range(len(snake.pos_x)):
				if self.pos_x == snake.pos_x[i] and self.pos_y == snake.pos_y[i]:
					position_okay = False

  
	def draw(self):
		"""draw the food in the shape of a red square """
		x = int((self.pos_x * BLOCK_WIDTH) + BLOCK_MARGIN)
		y = int((self.pos_y * BLOCK_WIDTH) + BLOCK_MARGIN)
		w = int(BLOCK_WIDTH - (2 * BLOCK_MARGIN))
		pygame.draw.rect(screen, COL_FOOD, (x,y,w,w))

	def erase(self, p_x = 0, p_y = 0):
		"""erase the block from the canvas"""
		x = int((p_x * BLOCK_WIDTH) + BLOCK_MARGIN)
		y = int((p_y * BLOCK_WIDTH) + BLOCK_MARGIN)
		w = int(BLOCK_WIDTH - (2 * BLOCK_MARGIN))
		pygame.draw.rect(screen, COL_BACKGROUND, (x,y,w,w))


# create objects
snack = Food(COL_FOOD)
snake = Snake(COL_BACKGROUND)

# setup routine
snack.generate()
scores.loadScores()

# MAIN LOOP	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###	###
game_active = True
while game_active:
    # first, the input
	for event in pygame.event.get():
        #check for closing the window / end the game
		if event.type == pygame.QUIT:      # close window
			game_active = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			menu_active = True
			
		#key input
		if event.type == pygame.KEYDOWN:
			if menu_active:
				# input for menu
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					menu_i -= 1
				if event.key == pygame.K_s or event.key == pygame.K_DOWN:
					menu_i += 1
				if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
					menu_action = True
			else:
				# input for game
				if event.key == pygame.K_r:
					snack.generate()
				
				# direction control
				if (event.key == pygame.K_w or event.key == pygame.K_UP) and snake.direction != DOWN:
					snake.direction = UP
				if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and snake.direction != UP:
					snake.direction = DOWN
				if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and snake.direction != RIGHT:
					snake.direction = LEFT
				if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and snake.direction != LEFT:
					snake.direction = RIGHT
        
	# logic
	if menu_active:
		# menu logic

		# menu control
		if(menu_i < 0):
			menu_i = len(menu_points) - 1
		if(menu_i >= len(menu_points)):
			menu_i = 0

		# actions
		if menu_action:
			menu_action = False
			if(menu_i == 0):			# "PLAY"
				menu_active = False				# leave menu
				snake.reset()					# reset snake
				screen.fill(COL_BACKGROUND)		# clear the background
				snack.generate()				# generate new snake
				blocks_per_second = initial_blocks_per_second		# set velocity
				update_time = 1 / blocks_per_second
				points = 0						# set points to zero
			elif(menu_i == 1):			# setting: wall boundary
				set_wall_boundaries = not(set_wall_boundaries)					# toggle setting
				menu_points[menu_i] = "wall boundaries: " + str(set_wall_boundaries)	# adapt text
			elif(menu_i == 2):			# setting: increase speed
				set_increase_velocity = not(set_increase_velocity)				# toggle setting
				menu_points[menu_i] = "increase speed: " + str(set_increase_velocity)	# adapt text
			elif(menu_i == 3):			# "QUIT"
				game_active = False
			
	else:
		# move the snake
		time_now = time.time()
		if(last_time + update_time <= time_now):
			snake.move()
			if(snake.plan_add_block == True):
				snake.addBlock()
				snake.plan_add_block = False
			last_time = time.time()
    
	# draw
	if menu_active:
		screen.fill(COL_BACKGROUND)		# clear screen

		# draw score
		height = int(42.667 * MULTIPLIER)		# initial height of text. the value will be increased for following lines

		# format the text for score and highscore
		score_text = str(points) + " pt"
		highscore_text = ""
		
		if(points == 0):
			score_text = "SNAKE"
		else:
			if(points > 1):
				score_text += "s"

		# draw scores line
		score_text_surface, score_surface_rect = menu_font.render(score_text, COL_MENU_NORMAL, COL_BACKGROUND, pygame.freetype.STYLE_DEFAULT, 0, int(64 * MULTIPLIER))
		screen.blit(score_text_surface, ((SCREEN_WIDTH/2) - (score_surface_rect.width/2), height))
		
		name, hs = scores.getHighscore()
		if(points > 0) and (name != None):
			highscore_text += "(HS: " + str(hs) + "pts)"

			height += score_surface_rect.height + int(16 * MULTIPLIER)			# calculate the starting height for the highscore

			# draw highscore line
			highscore_text_surface, highscore_surface_rect = menu_font.render(highscore_text, COL_MENU_NORMAL, COL_BACKGROUND, pygame.freetype.STYLE_DEFAULT, 0, int(20 * MULTIPLIER))
			screen.blit(highscore_text_surface, ((SCREEN_WIDTH/2) - (highscore_surface_rect.width/2), height))

			height += highscore_surface_rect.height + int(42.667 * MULTIPLIER)		# calculate the starting height for the menu
			# 			  								L> gap between score and menu
		else:
			height += score_surface_rect.height + int(42.667 * MULTIPLIER)			# compensate for not calculated gap between score and menu

		space = int(16 * MULTIPLIER) # gap between menu points
		#draw menu
		for i, text in enumerate(menu_points):
			# regulate some settings
			col_text_fg = COL_MENU_NORMAL
			if(i == menu_i):		# highlighting the text if selected
				col_text_fg = COL_MENU_HIGHLIGHTED
				text = "[ " + text + " ]"

			# render text
			text_surface, rect = menu_font.render(text, col_text_fg, COL_BACKGROUND, pygame.freetype.STYLE_DEFAULT, 0, int(20 * MULTIPLIER))

			# blit the text to the screen
			screen.blit(text_surface, ((SCREEN_WIDTH/2) - (rect.width/2), height))

			height += space + rect.height
	else:
		screen.fill(COL_BACKGROUND)
		# draw the game
		snack.draw()
		snake.draw()

	pygame.display.flip()

	# collision
	if(menu_active == False):
		game_lost = False
		# snake eating snack
		if snack.pos_x == snake.pos_x[0] and snack.pos_y == snake.pos_y[0]:
			pygame.mixer.Sound.play(SFX_EAT)
			snack.generate()						# create new snack
			snake.plan_add_block = True				# let the snake grow
			points += 1								# count the points
			if set_increase_velocity:		# if acceleration is activated:
				blocks_per_second += acceleration
				update_time = 1 / blocks_per_second		# recalculate the update time
		
		# snake running in itself
		no_collision = True
		for i in range(1, len(snake.pos_x)-1, 1):
			if snake.pos_x[i] == snake.pos_x[0] and snake.pos_y[i] == snake.pos_y[0]:
				no_collision = False
		
		if(no_collision == False):
			game_lost = True
		
		# with the head through the wall
		if(set_wall_boundaries == True):
			# first the x axis
			if(snake.pos_x[0] < 0):
				game_lost = True
			elif(snake.pos_x[0] >= BLOCKS_X):
				game_lost = True
			# now the y-axis
			if(snake.pos_y[0] < 0):
				game_lost = True
			elif(snake.pos_y[0] >= BLOCKS_Y):
				game_lost = True
		
		if game_lost:
			pygame.mixer.Sound.play(SFX_DIE)
			menu_active = True

	clock.tick(FPS)

print(str(SCREEN_WIDTH) + "|" + str(SCREEN_HEIGHT))
pygame.quit()
