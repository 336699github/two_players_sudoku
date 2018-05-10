

import PodSixNet.Channel
import PodSixNet.Server
import sys, os, random, pygame
from time import sleep
sys.path.append(os.path.join("objects"))
import SudokuGrid

class ClientChannel(PodSixNet.Channel.Channel):
    #def Network(self,data):
        #print data
        #print "at ClientChannel.Network"


    def Network_startgame(self,data):
        #print data
        num=data["num"]
        self.gameid=data["gameid"]
        self._server.startgame(num,self.gameid,data)

    def Network_place(self,data):
        #print "at ClientChannel.Network_place"
        #print "received message",data
        #deconsolidate all of the data from the dictionary
        x=data["x"]
        y=data["y"] 

        number=data["number"]
    
        #player number 1 or 0
        num=data["num"]

        #id of game given by server at start of game 
        self.gameid=data["gameid"]

        #mark to be added for this turn 
        mark_to_add=data["mark_to_add"]

        #tells server to place the digit
        self._server.placeDigit(x,y,number,data,self.gameid,num,mark_to_add)
    def Network_switchTurn(self,data):
        #print "at ClientChannel.Network_switchTurn"
        self.gameid=data["gameid"]
        self._server.switchTurn(self.gameid,data)


    def Close(self):
        self._server.close(self.gameid)

#manager of the state of the game, keep each client updated about what to display 
class SudokuServer(PodSixNet.Server.Server):
    def __init__(self,*args,**kwargs):
        PodSixNet.Server.Server.__init__(self,*args,**kwargs)
        self.games=[]
        self.queue=None
        self.currentIndex=0


    channelClass=ClientChannel

    def Connected(self,channel,addr):
        #print 'new connection:',channel
        #if there is currently no active game waiting for the other player 
        #then create a game with Game(), assign to the queue (self.queue now represent a Game object)
        if self.queue==None: 
            
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel,self.currentIndex)
            #print self.queue.sudoku_grid
        #if there is already a game in the queue,waiting for an opponent 
        #add the player to the game 
        #send message to the Client 
        else:
            sudoku_grid=self.queue.sudoku_grid
            #print sudoku_grid
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            
            self.queue.player0.Send({"action":"connectGame","player":0,"gameid":\
                self.queue.gameid,"puzzle_grid":sudoku_grid.puzzle_grid,"solution_grid":sudoku_grid.solution_grid})
            self.queue.player1.Send({"action":"connectGame","player":1,"gameid":\
                self.queue.gameid,"puzzle_grid":sudoku_grid.puzzle_grid,"solution_grid":sudoku_grid.solution_grid})
            
            self.games.append(self.queue)
            self.queue=None
            
    def startgame(self,num,gameid,data):
        game=[a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].startgame(num,data)
    def placeDigit(self,x,y,number,data,gameid,num,mark_to_add):
        #print "at SudokuServer.placeDigit"
        game=[a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].placeDigit(x,y,number,data,num,mark_to_add)

    def switchTurn(self,gameid,data):
        game=[a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].switchTurn()

    def close(self,gameid):
        try: 
            game=[a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
            game.player1.Send({"action":"close"})
        except:
            pass 


#represent the state of the game
class Game:
    def __init__(self,player0, currentIndex):

        #initialize the empty puzzle grid 
        self.sudoku_grid=SudokuGrid.SudokuGrid()
        #create the puzzle and solution grid
        self.sudoku_grid.create_grid()

        #whose turn 1 or 0
        self.turn=0
        #keep track of the mark of each player 
        self.player_mark=[0,0]

        #initialize the players including the one who started the game
        self.player0=player0
        self.player1=None

        #gameid of game
        self.gameid=currentIndex
    def startgame(self,num,data):
        #who started the game 
        self.turn=num
        self.player0.Send({"action":"startGame","TorF":True if num==0 else False })
        self.player1.Send({"action":"startGame","TorF":True if num==1 else False })

    def placeDigit(self,x,y,number,data,num,mark_to_add):
        #print "at Game.placeDigit, with message:",data 
        #make sure it's their turn 
        if num==self.turn:
            
            #place digit in game
            self.sudoku_grid.puzzle_grid[y][x]=number


            #add mark to corresponding player 
            self.player_mark[num]+=mark_to_add



            #send data and turn data to each player 
            self.switchTurn()
            
            self.player0.Send(data)
            self.player1.Send(data)

            self.player0.Send({"action":"win" if num==0 else "lose","mark_to_add":mark_to_add})
            self.player1.Send({"action":"win" if num==1 else "lose","mark_to_add":mark_to_add})

            #print "self.sudoku_grid.puzzle_grid",self.sudoku_grid.puzzle_grid
            #if boards are all filled, decide who won the game 
            if self.sudoku_grid.puzzle_grid==self.sudoku_grid.solution_grid:
                #print "the grid has been completed"
                self.player0.Send({"action":"gameover" ,"didiwin":True if self.player_mark[0]>self.player_mark[1] else False})
                self.player1.Send({"action":"gameover" ,"didiwin":True if self.player_mark[1]>self.player_mark[0] else False})

    def switchTurn(self):
        #print "at game.switchTurn"
        self.turn=0 if self.turn else 1
        self.player0.Send({"action":"yourturn","TorF":True if self.turn==0 else False})
        self.player1.Send({"action":"yourturn","TorF":True if self.turn==1 else False})


#print "STARTING SERVER ON LOCALHOST"
sudoku_server=SudokuServer()
while True:
    sudoku_server.Pump()
    sleep(0.01)
