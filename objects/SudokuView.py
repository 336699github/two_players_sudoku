import sys, os, pygame
sys.path.append(os.path.join("objects"))
import Button
import Timer 
import SudokuSquare
from GameResources import *
						

WHITE=(255,255,255)
BLACK=(0,0,0)        
				   
class SudokuView:

##############initiation functions #######################


	def init_graphics(self):

		self._redindicator,_=load_image("redindicator.png")
		self._greenindicator,_=load_image("greenindicator.png")
		self._winningscreen,_=load_image("youwin.png")
		self._gameover,_=load_image("gameover.png")
		self._score_panel,_=load_image("score_panel.png")

	def init_music(self):
		load_music("chopin.wav")
		

	def init_board(self):
		size=WIDTH, HEIGHT = 400, 600
		#initialize the screen
		self._screen= pygame.display.set_mode(size)
		pygame.display.set_caption("SUDOKU")
	  
		#set background image (grid pattern)
		self._background = pygame.Surface(self._screen.get_size())
		self._background = self._background.convert()
		self._background.fill(WHITE)

		self._board, self._boardRect = load_image("SudokuBg.png")
		self._boardRect = self._boardRect.move(10, 80)


		self._screen.blit(self._background, (0, 0))
		self._screen.blit(self._board, self._boardRect)

		
	def init_squares(self):
		 #initialize the squares with all '0' value and editable, define the position of each square
		self._squares=[]
		

		initXLoc = 10
		initYLoc = 80
		startX, startY, editable, number = 0, 0, "Y", '0'
		for y in range(9):
			for x in range(9):
				if x in (0, 1, 2):  startX = (x * 41) + (initXLoc + 2)
				if x in (3, 4, 5):  startX = (x * 41) + (initXLoc + 6)
				if x in (6, 7, 8):  startX = (x * 41) + (initXLoc + 10)
				if y in (0, 1, 2):  startY = (y * 41) + (initYLoc + 2)
				if y in (3, 4, 5):  startY = (y * 41) + (initYLoc + 6)
				if y in (6, 7, 8):  startY = (y * 41) + (initYLoc + 10)
				
				self._squares.append(SudokuSquare.SudokuSquare(number, startX, startY, editable, x, y))
		#start by highlight the first square. 
		self.currentHighlight = self._squares[0]
		self.currentHighlight.highlight()
	def __init__(self):
		pygame.init()
		pygame.font.init()
		
		self.theNumbers = { pygame.K_0 : "0", pygame.K_1 : "1", pygame.K_2 : "2",\
		pygame.K_3 : "3", pygame.K_4 : "4", pygame.K_5 : "5",\
		pygame.K_6 : "6", pygame.K_7 : "7", pygame.K_8 : "8",\
		pygame.K_9 : "9", pygame.K_SPACE : "", pygame.K_BACKSPACE : "",\
		pygame.K_DELETE : "" }

		self.init_graphics()
		#self.init_music()
		self.init_board()
		self.init_squares()
		self._button=Button.Button(self._screen)
		self.timer=Timer.Timer(self._screen)

		
		self.turn=False
		self.my_mark=0
		self.otherplayer_mark=0




########  drawing functions  #################

	def _draw_board(self):
		#draw the background and board
		self._screen.blit(self._background, (0, 0))
		self._screen.blit(self._board, self._boardRect)

	def _draw_squares(self):
		#draw the squares
		for square in self._squares:
			square.draw()

	def _draw_HUD(self):
		#draw the background for the bottom:
		self._screen.blit(self._score_panel,[0,500])

		#create font 
		myfont=pygame.font.SysFont(None, 32)

		#create text surface
		label=myfont.render("Your Turn:",1,WHITE)

		#draw surface
		self._screen.blit(label,(10,500))

		self._screen.blit(self._greenindicator if self.turn else self._redindicator,(130,500))


		myfont64 = pygame.font.SysFont(None, 64)
		myfont20 = pygame.font.SysFont(None, 20)
 
		scoreme = myfont64.render(str(self.my_mark), 1, WHITE)
		scoreother = myfont64.render(str(self.otherplayer_mark), 1, WHITE)
		scoretextme = myfont20.render("You", 1, WHITE)
		scoretextother = myfont20.render("Other Player", 1, WHITE)
 
		self._screen.blit(scoretextme, (10, 525))
		self._screen.blit(scoreme, (10, 535))
		self._screen.blit(scoretextother, (280, 525))
		self._screen.blit(scoreother, (280, 535))



	def _draw_all(self):
		#clear the screen
		self._screen.fill(0)

		self._draw_board()
		self._draw_squares()
		self._draw_HUD()
		self._button.draw()
		self.timer.draw()

########## register listener ######################

	def register_listener(self,controller):
		self._button.add_action_listener(controller)
		self.timer.add_action_listener(controller)
		for square in self._squares:
			square.add_action_listener(controller)




		
######### function for model to change view #########
	def _get_square(self,x,y):
		#return the square object at location x,y 
		for square in self._squares:
			if square.currentLoc()==(x,y):
				return square

	def change_square(self,x,y, number):
		self._get_square(x,y).change(number)

	def _listen_for_event(self):
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit()
			if event.type==pygame.USEREVENT and self.turn:
				if self.timer.update()=="time_is_up":
					self.timer.time_is_up()

			
			if event.type == pygame.MOUSEBUTTONDOWN:
				mousepos = pygame.mouse.get_pos()
				#if clicked on the button 
				if self._button.check_collide(mousepos):
					self._button.go_button_clicked()
	
				#if clicked on one of the squares
				for current_square in self._squares:
					if current_square.check_collide(mousepos):
						self.currentHighlight.unhighlight()
						self.currentHighlight = current_square
						self.currentHighlight.highlight()
			#if user entered a digit 
			if event.type == pygame.KEYDOWN and event.key in self.theNumbers and self.turn==True:
				self.currentHighlight.enter_digit(self.theNumbers[event.key],self.timer.get_time_left())
			

######### update function **********
	def update(self):
		self._draw_all()
		self._listen_for_event()
		pygame.display.flip()

	def game_over(self,didiwin):
		print "at SudokuView.game_over"
		self._screen.blit(self._winningscreen if didiwin else self._gameover,(8,0))
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					exit()
			pygame.display.flip()
		
		 




