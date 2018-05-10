import random
import sudoku_solver_short

class SudokuGrid:
	"""A class to generate and check Sudoku data."""
	def __init__(self):
		"""Builds two default, totally empty grid.
		one for puzzle, one for the solution"""
		self.puzzle_grid = []
		temp = []
		for x in range(9):
			temp.append('0')
		for y in range(9):
			self.puzzle_grid.append(temp[:])

		self.solution_grid=self.puzzle_grid[:][:]

	  
	def _print_grid(self,grid):
		"""Provides a print for debugging at the console."""
		print
		for x in range(9):
			for y in range(9):
				if y in (3, 6):
					print "|",
				temp = grid[x][y]
				if temp == None:
					print " ",
				else:
					print temp,
			if x in (2, 5):
				print
				print "-" * 22
			else:
				print
		print

	def create_grid(self, Seed=None):
		"""Randomly choose from a group of preset puzzles"""
		#TODO: input a list of sudoku puzzles from a text file, randomly select one
		#random.seed(Seed)
		puzzle="003020600900305001001806400008102900700000008006708200002609500800203009005010300"
		for num in range(len(puzzle)):
			self.puzzle_grid[num/9][num%9]=puzzle[num]
		self._print_grid(self.puzzle_grid)
		#use sudoku_solver_short to obtain the solution 
		self.solution_grid=sudoku_solver_short.get_solution_grid(puzzle)

		self._print_grid(self.solution_grid)

	
	def is_correct(self, row,column,number):
		if  not self.solution_grid[row][column] == number:
			print "wrong number! "
			print "should be :",self.solution_grid[row][column]
			print "you entered: ",number 
			return False
		return True
	

if __name__ == "__main__":
	print "Testing SudokuGrid functionality."
	print "Create an empty grid..."
	sample_grid = SudokuGrid()

	print "create a puzzle "
	sample_grid.create_grid()
   

