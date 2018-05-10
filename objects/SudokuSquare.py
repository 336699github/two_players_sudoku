import pygame

class SudokuSquare:
	"""A sudoku square class."""
	def __init__(self, number=None, offsetX=0, offsetY=0, edit="Y", xLoc=0, yLoc=0):
		if number != '0':
			number = str(number)
		else:
			number = ""
		
		self._font = pygame.font.Font(None, 30)
		self._text = self._font.render(number, 1, (0, 0, 0))
		self._textpos = self._text.get_rect()
		self._textpos = self._textpos.move(offsetX + 12, offsetY + 6)

		self._collide = pygame.Surface((40, 40))
		self._collide = self._collide.convert()
		self._collide.fill((255, 255, 255, 255))
		self._collideRect = self._collide.get_rect()
		self._collideRect = self._collideRect.move(offsetX + 1, offsetY + 1)
		# The rect around the text is 11 x 28

		self._edit = edit
		self._xLoc = xLoc
		self._yLoc = yLoc


	def draw(self):
		screen = pygame.display.get_surface()
		screen.blit(self._collide, self._collideRect)
		screen.blit(self._text, self._textpos)


	def check_collide(self, mousepos):
		if len(mousepos) == 2:
			return self._collideRect.collidepoint(mousepos)
		elif len(mousepos) == 4:
			return self._collideRect.colliderect(mousepos)
		else:
			return False


	def highlight(self):
		self._collide.fill((190, 190, 255))
		self.draw()


	def unhighlight(self):
		self._collide.fill((255, 255, 255, 255))
		self.draw()


	def change(self, number):
		if number != '0':
			number = str(number)
		else:
			number = ""
		
		if self._edit == "Y":
			self._text = self._font.render(number, 1, (0, 0, 0))
			self._edit="N"
			self.draw()
			return 0
		else:
			return 1


	def currentLoc(self):
		return self._xLoc, self._yLoc

	def add_action_listener(self,controller):
		self._controller=controller
	def enter_digit(self,number,mark):
		x, y = self.currentLoc()
		self._controller.enter_digit(x,y,number,mark)
		