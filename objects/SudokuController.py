
import pygame 
from PodSixNet.Connection import ConnectionListener, connection 
from time import sleep 

class SudokuController(ConnectionListener):
	def __init__(self,model):
		#pygame.mixer.init()
		self._model=model
		##self._beep_sound=pygame.mixer.Sound("beep.wav")
		self._connected=False
		self.Connect()
		while not self._connected:
			self.Pump()
			connection.Pump()
			sleep(0.01)
		

	def go_button_clicked(self):
		if not self._model.game_is_on:
			self.Send({"action":"startgame","gameid":self._model.gameid,"num":self._model.player_num})

	def enter_digit(self,x,y,number,mark):
		if self._model.is_correct(x,y,number):
			self.Send({"action":"place","x":x,"y":y,"number":number,\
						"gameid":self._model.gameid,"num":self._model.player_num,"mark_to_add":mark})
			self._model.update(x,y,number)
		else:
			self._model.enter_wrong_digit()
			#self._beep_sound.play()
		
	def time_is_up(self):
		self.Send({"action":"switchTurn","gameid":self._model.gameid}) 

	def Network_connectGame(self,data):
		self._connected=True
		self._model.player_num=data["player"]
		self._model.gameid=data["gameid"]
		#receive the puzzle_grid and solution_grid from server
	   
		self._model.sudoku_grid.puzzle_grid=data["puzzle_grid"]
		self._model.sudoku_grid.solution_grid=data["solution_grid"]
		#pygame.mixer.music.play(-1, 0.0)
		print "connected game:",self._model.gameid, "for player: ",self._model.player_num

	def Network_startGame(self,data):
		self._model.start_game(data["TorF"])

	def Network_place(self,data):
		print "at SudokuClient.Network_place"
		#get attributes
		x=data["x"]
		y=data["y"] 
		number=data["number"]
		self._model.update(x,y,number)
		print "placing ",number,"at row:",y,"column:",x

	def Network_win(self,data):
		self._model.win(data["mark_to_add"])

	def Network_lose(self,data):
		self._model.lose(data["mark_to_add"])

	def Network_yourturn(self,data):
		self._model.switch_turn(data["TorF"])

	def Network_gameover(self,data):
		self._model.game_over(data["didiwin"])
	def Network_close(self,data):
		exit()

	def update(self):
		connection.Pump()
		self.Pump()
		






  





