import pygame 

class Timer:
	def __init__(self,screen):
		self._screen=screen
		self._counter=30
		self._text=str(self._counter).rjust(3)
		pygame.time.set_timer(pygame.USEREVENT,1000)
		self._font=pygame.font.SysFont(None,30)
		self._screen.blit(self._font.render(self._text,True,(0,0,0)),(280,20))

	def reset(self):
		self._counter=30

	def reduce_time(self,time):
		self._counter-=time

	def get_time_left(self):
		return self._counter

	def draw(self):
		self._text=str(self._counter).rjust(3)
		self._screen.blit(self._font.render(self._text,True,(0,0,0)),(280,20))
		pygame.display.flip()

	def update(self):
		
		#print "updating timer"
		self._counter-=1
		if self._counter>0:
			self._text=str(self._counter).rjust(3) 
			#print "text=",self._text
		else:
			self._text='boom!'
			return "time_is_up"
			
		self._screen.blit(self._font.render(self._text,True,(0,0,0)),(280,20))
		pygame.display.flip()

	def add_action_listener(self,controller):
		self._controller=controller
	def time_is_up(self):
		self._controller.time_is_up()

