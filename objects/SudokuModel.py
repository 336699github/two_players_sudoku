import SudokuGrid
import pygame


		
class SudokuModel:

	def __init__(self,view):
		self._view=view
		
		self.sudoku_grid=SudokuGrid.SudokuGrid()

		self.game_is_on=False
		
		
		self.gameid=None
		self.player_num=None


	def start_game(self,turn):
		self.game_is_on=True
		self._view.turn=turn
		self._view.timer.reset()
		#UPDATE VIEW WITH INITIAL PUZZLE_GRID 
		for x in range(9):
			for y in range(9):
				number=self.sudoku_grid.puzzle_grid[y][x]
				if number!='0':
					self._view.change_square(x,y,number)
		print "starting game with :","me" if self._view.turn else "other player"
	

	def update(self,x,y,number):
		
		self.sudoku_grid.puzzle_grid[y][x]=number
		self._view.change_square(x,y,number)
		

		
	def is_correct(self,x,y,number):
		return self.sudoku_grid.is_correct(y,x,number)


	def enter_wrong_digit(self):
		self._view.timer.reduce_time(5)


	def win(self,mark):
		print "add",mark ,"to me"
		self._view.my_mark+=mark
	def lose(self,mark):
		print "add", mark, "to the other player"
		self._view.otherplayer_mark+=mark

	def switch_turn(self,turn):
		self._view.turn=turn
		self._view.timer.reset()

	def game_over(self,didiwin):
		print "at SudokuModel.game_over"
		self._view.game_over(didiwin)


