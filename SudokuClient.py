#!/Users/luliu/anaconda/bin/python
import sys,os,pygame
sys.path.append(os.path.join("objects"))
import SudokuView
import SudokuController 
import SudokuModel


class SudokuClient:

    
    def __init__(self):
        #initialize pygame clock, tracking time in the game 
        self.clock=pygame.time.Clock()
        self.view=SudokuView.SudokuView()
        self._model=SudokuModel.SudokuModel(self.view)
        self.controller=SudokuController.SudokuController(self._model)
        self.view.register_listener(self.controller)
        

        
sudoku_client=SudokuClient()

while True:
    sudoku_client.clock.tick(60)
    sudoku_client.view.update()
    sudoku_client.controller.update()
        

